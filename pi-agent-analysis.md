# Pi 审核与修复效率优化方案（历史目标架构）

> 状态：历史设计参考，已被 Paseo 轻量编排取代；不是当前实施基线、运行手册或 backlog。
> 当前角色、路由、外发边界和完成条件以 `AGENTS.md`、`.ai/roles/` 与
> `docs/paseo-orchestration-v2-contract.md` 为准。本文的 `tools/i18n audit` CLI、campaign
> 状态机和缓存／修复编排均未作为当前入口实现，不得按下文命令执行。

- 2026-08-08 的 pi coding agent／旧项目 subagent 路由已经归档；历史表述仅用于理解当时
  的设计动机，不代表当前可用能力。
- 日期：2026-08-01
- 审阅依据：`review.md` 第六稿；前序 Codex 内置审阅；此前“高效性与闭环性”独立审阅；第九、十轮
  独立无上下文审阅
- 本轮处置：IR9-001–IR9-011 均已落实；IR10-001–IR10-005 均接受，但按能力启用点处置：
  candidate-influenced 进程 sandbox 与统一 plan generation transition 是对应高级能力的硬门槛；MVP
  禁用 candidate 自动执行、动态 split/merge、多 task 自动终止和动态重包，因此这些缺口不阻塞只读审核。
  重点新增 event crash-atomic installer、per-key cache singleflight/serializable classification、
  attempt+result composite、termination 笛卡尔归约、campaign-neutral candidate effect、exact host
  composite、work-unit lineage identity、conserved entitlement、跨进程 provider slot、remediation
  状态机与预创建 follow-up responsibility

## 1. 背景与结论

当前 Pi 流程把 bundle 生成、审核、remediation、人工应用和复审拆成彼此独立的
一次性命令。每一步都能单独校验，但缺少统一 campaign、精确缓存、覆盖率状态、
finding 生命周期和修复后闭环，因此小范围修改也容易触发重复生成、重复调用和人工串联。

本方案的核心不是扩大 Pi 权限，而是在保留安全边界的前提下，把现有命令组织成一个
可恢复、可缓存、可证明完成的审核系统：

```text
内容快照
   ↓
增量 Planner ──→ 内容寻址对象库
   ↓                    ↓
Review Campaign → Runner / Cache
   ↓
Finding Ledger
   ↕ 显式 reply / disposition artifact
Codex 答复 ←→ 无会话 Pi 复核
   ↓
候选修订 → 本地校验 → 主代理应用
   ↓
定向测试与增量复审 → Verified / Waived / Disputed
```

本轮修订把此前“概念上存在但主路径不可达”的部分收敛为以下可执行不变量：

- 本地 cache attach 先于外部转移授权；只有 miss、`--force` 或要求 fresh execution 的独立终审才
  请求外发授权。
- Candidate 必须经过 `validated → accepted generation → applied → current-revision reply → re-review`；
  任一步都不能靠文档推断或 SQLite 指针代替事件。
- Task 重分包、合并和派生删除必须形成 lineage DAG；历史 task 只有在 successor 覆盖证明完成后
  才能进入成功终态。
- 一个冻结的语义审核实例可以有多个严格串行的 transport attempt，但只能接受一个 validated result；
  continuity ordinal、payload-repair generation 和 independent-final generation 分开计数。
- Task/campaign 的终止先进入 draining，所有 attempt、reservation 和 round 都结算后才可 terminal。
- 整轮 disposition 是一个原子事件；同 cache key 的非等价 validated observation 会使 key 冲突并
  阻止自动通过。
- 所有 event 只可由完整 pending file 经 fsync 与 no-replace 原子安装成为 chain 成员；最终路径永不
  暴露半写文件。
- 同一 cache key 的 miss/force/classification/attach/resolve/completion 由一个权威 generation 和
  singleflight 串行化；validated attempt terminal 与业务 result acceptance 不再分成不可恢复的两事件。
- Lineage node 使用不可复用 work-unit instance，split/merge 只建立 generation 递增 edge，并守恒
  continuity/final/remediation/repair/force entitlement。
- 默认 exact 模式的人工修复通过一次性完整 reauthorization+plan acceptance composite 可达；额外
  remediation 和 terminal follow-up 都有显式 request、责任与 CLI 闭环。

### 1.1 实施决策：先使用，再按证据扩展

本文后续完整 campaign、lineage、candidate、并发和 GC 契约继续作为目标架构，但不再要求全部实现后
才能使用 Pi。个人维护项目的首版冻结为以下 MVP：

- 单用户、单 writer、`concurrency=1`；每次必须显式选择 `code` 或 `translations`，不默认全量；
- 固定 bundle 边界，精确内容命中直接复用已严格校验的结果；不动态 split/merge，也不组合不同 bundle
  的审核结论；
- Pi 每次以 `--no-session --no-tools` 新进程运行，只返回 findings；finding ref、缓存身份和 schema
  归一化均由宿主完成；
- Pi 输出中的 patch、命令或可执行内容一律只视为文本建议。MVP 不自动应用，也不运行任何受该输出影响的
  test、lint、LuaJIT load、hook 或 formatter；
- 修订由 Codex/维护者独立完成，随后对最新有界 bundle 重新审核。Clean 通常 1 次外发，有修订通常
  2 次；达到 3 轮仍未收敛则显式停止或升级；
- 首版只实现 immutable artifact、严格输出、精确缓存、调用/耗时记录和人工可检查的闭环证据；不实现
  动态 lineage、remediation 自动化、跨进程并发、公平排队或 GC execute。

以下能力具有硬启用门槛，不能因“个人项目”而静默放宽：

1. 启用 candidate 自动验证前，必须满足第 4.3 节 candidate-influenced process sandbox，并通过恶意
   candidate 无法读取受保护 root/凭据、写真实工作区或联网的退出测试；
2. 启用任何会改变 `plan_generation` 的同 campaign 修订前，必须实现第 6.1 节统一
   `plan-generation-transition`，包括普通 1→1 predecessor/successor；
3. 启用 split/merge 前，必须满足第 6.2 节 history-equivalent 条件和稳定 packing 规则；
4. 启用多 task 自动终止前，必须实现 child work-unit terminal cascade；
5. 只有真实运行数据证明单进程吞吐不足时，才进入跨进程 admission 与 Phase 4 优化。

MVP 连续运行 10–20 个真实审核任务后，以调用次数、cache hit、schema 失败率、误报率、人工暂停次数和
平均收敛轮数决定下一项能力；不再以继续增加纸面状态作为实施进展。

## 2. 已观察到的效率基线

以下数据来自 2026-08-01 本地 artifact 元数据，不展开 bundle 正文。历史“调用数”以运行时记录中
启动 `opencode-go` provider 的 attempt 为单位，包括再次启动的 retry，排除 `fixture`、只在本地执行
的 wrapper/validator 和中间 artifact；因此目录数量不能直接当作外部调用数。新 schema 不再把
`external-transfer-started` 等同于 provider 已确认收到请求：该事件只证明“可能已外发且应保守计费”，
报告会分开统计 `charged_or_possible_transfers`、`provider_request_confirmed` 和 `validated_results`：

- 32 次审核调用中 6 次失败。
- 22 次 remediation 调用中 3 次失败。
- 2 次翻译调用中 1 次失败。
- 合计 56 次外部调用，10 次没有产生可用结果，失败率约为 17.9%。
- 其中 6 次失败来自 schema、contract、`item_id` 或路径绑定错误；这些属于本地协议层问题。
- 27 个 review index 共引用 3,135 个 bundle，但只有 1,257 个唯一 bundle；约 60% 为重复引用。
- 曾有 5 次全量 review 生成，每次产生 609 个翻译 bundle；共生成 3,045 次翻译 bundle
  引用，而真实记录中只执行过 1 次翻译 bundle 审核。
- `.artifacts/i18n` 约为 190 MiB，其中 review artifact 约为 96.6 MiB。
- 60 条有效 finding 中，39 条为 minor、11 条为 note；只有 9 条 major 和 1 条 blocker。
- 19 次成功的代码 remediation 产生 56 个 proposal，其中 51 个为代码 patch，5 个为
  `no-change`；该口径不含另一路径的 24 个 `replace-translation`。
- 最后一次 remediation 后没有对应的新 validated review artifact，系统无法证明最终闭环。

这些现象说明首要收益来自范围控制、精确失效、缓存和协议适配，而不是提高并发。

## 3. 目标与非目标

### 3.1 目标

- 未改变的内容不重新生成 bundle，也不重新调用 Pi。
- 每次外发都绑定明确授权范围，并能追溯 provider、model、内容类型和调用预算。
- 模型不负责复制确定性的 schema、contract、长哈希或绝对路径。
- 审核、finding、候选修订、实际应用和最终验证形成可查询的状态链。
- Codex 可以围绕稳定 finding 进行逐项修复、反驳和补证；每轮输入输出均可重放和审计。
- 默认只审核变更和高风险项；全量审核必须显式请求。
- 测试与真实 artifact 完全隔离。
- 保留现有受保护输入边界，任何优化不得扩大 Pi 对闭源 DLC 的访问能力。

### 3.2 非目标

- 不让 Pi 直接修改规范 Lua、Python、配置或其他共享工作区文件。
- 不让 Pi 直接读取仓库、Shell、网络、会话历史或受保护输入。
- 不以 `pi --session`、`pi -c`、RPC 长连接或“最近 session”实现规范审核连续性。
- 不自动接受通过机械测试的语义修改。
- 不用缓存授权任何新的外部传输或扩大本地可读范围；精确 cache hit 本身不发生外发，因此不要求
  创建外部转移授权。
- 不在第一阶段自动删除历史 artifact。

## 4. 信任边界

### 4.1 Pi 默认无直接工具

Pi 只能读取显式 bundle，不能调用文件、Shell、Git、网络或项目工具。这样可以：

- 保证审核输入可复现、可哈希和可缓存；
- 防止提示注入诱导 Pi 扩大范围；
- 防止意外接触受保护 DLC、凭据或未授权文件；
- 让每条 finding 都能绑定到具体证据。

缺少上下文时不开放工具，而是使用受控证据请求协议，见第 9 节。

### 4.2 无隐式持久会话

`no-session` 不等于禁止多轮交流，而是禁止 bundle 之间共享不可见历史。审核连续性属于
Review Campaign，不属于 Pi 进程或 session。每一轮 Pi 都以新进程、`--no-session`、`--no-tools`
和无项目上下文运行；它只能看到本轮经过校验的有界 bundle。

允许的多轮必须显式记录为 campaign artifact：

```text
当前有界快照 → 初审 findings → Codex 逐项答复/修订/补证
      ↑                                      ↓
      └──────── 新 revision 的复核 bundle ←─┘
                         ↓
       resolved | still_open | disputed | new finding
```

禁止通过查找最新 session、复用 `sessionFile`、`pi -c` 或 RPC 进程记忆传递审核状态。否则旧工具
输出、隐藏消息或并发串线会影响结果，却不进入 bundle digest、授权范围和缓存键，令结果无法
复现。Pi“重新读取最新代码”的含义只能是读取宿主重新生成的最新有界 bundle，不能自行访问工作区。

普通代码 campaign 的最短路径是一轮：初审 clean 且没有候选应用、答辩或补证时直接进入本地完成
gate，不制造无意义“最终复审”。只有内容改变、需要答辩/补证或高风险独立终审时才创建后续实例。
Continuity 语义判断默认最多三轮；达到上限仍无法一致时进入确定性的
`awaiting-terminal-disposition`，由主代理/用户显式处置或创建 follow-up，不得无限追加上下文。

### 4.3 Pi 不写共享工作区

Pi 可以返回候选 patch 或翻译 proposal，但不能直接落盘。宿主 runner 可以在临时副本中：

- 检查 patch 与绑定 revision 是否一致；
- 执行 `git apply --check` 或等价的无写入检查；
- 试应用后运行定向测试和 lint；
- 生成供主代理审核的候选 artifact。

写入真实工作区仍由主代理完成，且写入后必须重新计算 revision 并进入复审。

“临时副本”本身不是执行隔离。任何 test、lint、LuaJIT load 或 import 只要会加载 candidate 影响的
内容，就视为执行不可信代码；在启用前必须由强制进程 sandbox 同时保证：受保护 root 不可见且不可读、
真实工作区只读、仅一次性临时根可写、网络和宿主 socket 禁止、环境变量/凭据与继承 fd 清空、解释器/
模块/可执行路径固定。平台不能证明这些条件时，只允许做 patch/schema/path/revision 的非执行检查，
不得以“只读测试”或“临时目录”替代隔离。MVP 明确采用后一模式，不执行 candidate-influenced 内容。

## 5. 效率优先的推荐基线

### 5.1 审核与候选修订尽量单次完成

Pi reviewer 一次返回 findings，并可为有把握的问题附带候选修订。默认不为每条 finding
自动调用独立 remediation。候选修订始终只是 `proposed`：同一次模型执行对自己候选的说明、
自检或测试建议均不构成独立复核，也不能自动写入共享工作区。

仅在以下情况启动额外 remediation：

- blocker 或 security finding；
- reviewer 明确标记低置信度或证据不足；
- 主代理无法独立判断候选修订；
- 用户明确要求第二意见。

满足触发条件并不等于可以直接运行低层命令；必须经过第 13.3 节 planned request、lineage entitlement、
cache-first、外发授权和预算/concurrency admission。默认每 lineage 最多一个 remediation semantic request，
没有候选需求时不为保持流程对称而调用。

minor/note 的机械候选可在单次审核中生成，但仍需主代理判断、本地校验及应用后的最终复审。
major、blocker 与 security 候选必须由未参与候选生成的执行进行最终复审：默认使用不同模型；
若无可用的第二模型，只能在用户明确授权后，使用无共享 session、独立 prompt 且不同 thinking
的同模型执行，并标记为 `degraded-independence`。相同 execution fingerprint 或共享历史的执行
一律不算独立；不同 alias 只有解析到不同、可验证的 canonical underlying `model_lineage_id` 才算默认独立。
复审 lineage 必须已包含在 campaign 授权中，否则先重新授权。

### 5.2 并发和预算

- 公开低风险代码/设计审核默认 authoritative active-attempt cap 为 2。
- 翻译与高风险安全审核默认 authoritative cap 为 1；cap 同时在 campaign authorization 和全局
  provider/risk pool 冻结，并由第 8.1 节跨进程 slot admission 执行，`--concurrency` 只可降低。
- 每个 campaign 默认最多 8 次外部调用。
- 单 task/single-bundle clean campaign 目标为 1 次调用；出现修订时通常为初审 + 应用后复审共 2 次；纯答辩/补证通常
  为初审 + continuity 复核共 2 次；答辩后再修订或高风险修订通常最多 3 次语义调用。
- Continuity 语义判断默认不超过三轮。独立终审、transport retry 和显式 payload repair 分别计入
  调用预算，但 retry/repair 不冒充新的 continuity round。
- 授权预览必须同时显示最短、预计和按已启用 stage/retry/repair 计算的最坏可达调用数；最坏值
  超过 campaign hard ceiling 时，必须减少可选重试/repair 或显式提高 ceiling，不能只展示“默认两次”。
- 并发只在缓存、精确失效和失败处理完成后启用。

Planner 对每个 plan/authorization generation 的冻结 stage graph 计算：

```text
max_reachable_calls =
  sum(max_transport_attempts for every reachable normal/continuity/final request)
  + sum(max_transport_attempts for every reachable payload-repair request)
  + sum(max_transport_attempts for every authorized forced-observation request)
```

分支互斥时取最大路径而不是盲目相加，是否互斥必须由状态机证明。默认 ceiling 8 可以覆盖“最多
3 个 continuity judgment + 1 个 independent final，且每个最多 2 次 transport attempt”的路径；若还
想对这些 request 全部启用 payload repair，最坏值会超过 8，授权前就必须关闭部分 repair/retry、降低
round/final 上限或明确提高 ceiling。普通 campaign 的 forced-observation total 默认为 0；启用 force
同样必须纳入公式。不能运行到一半才发现名义策略不可达。

令 `J` 为当前 generation 可达的 normal/continuity/final/remediation semantic requests，`F` 为授权的
forced observations。若每个 request/force 最多 2 个 transport attempts，则 retry-only 上界为
`2J + 2F`；若每个原请求都还可派生一个同样最多 2 attempts 的 payload repair，最坏为 `4J + 4F`。
Split/merge 后必须按第 6.2 节 conserved entitlement 重算 `J`，不能把 predecessor 的 remaining
request/final/repair slot 复制到每个 successor。新 graph 超出当前完整授权时先 reauthorize，再激活新
generation；默认 hard ceiling 8 仅在具体 graph 的证明值不超过 8 时才是可达配置。

### 5.3 审核范围

- 命令必须显式选择 `code`、`translations` 或二者；不再默认全选。
- 代码默认只审核公开工作区 diff。
- 翻译默认只审核变更条目、lint 风险项、待审术语和显式选择的周期性抽样。
- 全量翻译审核必须显式使用 `--all-translations`，并提前报告预计 bundle/token 数。

## 6. Review Campaign

### 6.1 Campaign 身份

文中所有 `sha256(field1 + field2 + ...)` 公式都只是逻辑字段列表，禁止实现为裸字节拼接。统一使用
`canonical-hash-v1`：每个对象先按带类型、长度和 domain tag 的确定性 framing 编码；字符串为 UTF-8，
bytes 保持原值，数组保序并带 count，map key 按 UTF-8 bytes 排序，每个 value 编码
`type_tag || u64be(length) || value_bytes`。最终计算：

```text
H(domain, object) = sha256(
  "tome4-i18n/canonical-hash-v1\0"
  || u64be(len(domain)) || domain
  || u64be(len(canonical_encode(object))) || canonical_encode(object)
)
```

任一字段、算法或 framing 改变都提升版本并令依赖 identity 精确失效。后文简写 `H(domain, {...})`；
任何实现若使用字符串连接、分隔符猜测或未标类型 JSON 都不符合本契约。Identity 对象只允许
`null`、bool、canonical signed integer、UTF-8 string、bytes、array 和 string-keyed map；拒绝重复 map
key、IEEE float、NaN/Infinity 和隐式 number/string 转换。费用等小数使用带 currency/scale 的 fixed-point
integer；若未来新增标量类型必须提升 framing 版本并提供跨语言 test vector。

内容身份与 campaign 实例身份分离。`plan_content_key` 只描述可复用内容，`campaign_id` 还描述为何
发起本次审核：

```text
plan_content_key = H("plan-content-v2", {
  scope,
  public_path_allowlist,
  planner_version,
  content_policy_digest,
  ordered_initial_task_revision_ids
})

campaign_id = H("campaign-v2", {
  plan_content_key,
  purpose,
  parent_campaign_id_or_null,
  campaign_request_event_digest,
  campaign_generation
})

plan_revision_id = H("plan-revision-v2", {
  campaign_id,
  plan_generation,
  ordered_current_task_revision_ids,
  dependency_digest
})
```

`purpose` 至少区分 `initial-change-review`、`periodic-review`、`waiver-expiry`、`false-positive-sample`、
`terminal-finding-follow-up` 和 `manual-rerun`。每次新 campaign 由 maintenance chain 中不可变的
`campaign-requested` event 触发；event 保存调用方提供的 idempotency key、purpose、parent 和 trigger
事实，`campaign_generation` 由 maintenance reducer 在
`(plan_content_key, purpose, parent_campaign_id)` 下单调分配，调用方不能自行重置。相同 idempotency
key/payload 重放复用同一 event/campaign；`campaign_request_event_digest` 是该 maintenance event
自身的 digest，不是调用方可伪造的 campaign ID 字段。新的周期触发或 follow-up 使用新的 request
event，不依赖时间戳也不会撞回已完成 campaign。`plan_content_key` 仍使相同内容
共享对象和语义缓存。

`task_id = H("review-task-v2", {bundle_kind, grouping_policy_version, ordered_item_ids})` 表示稳定任务
身份；`task_revision_id = H("task-revision-v2", {task_id, ordered_item_revision_hashes,
dependency_digest})`。item/item revision 均按 `item_id` 规范排序后聚合。
Task/task revision 是可复现的内容身份，不是 lineage node。每个 plan generation 中另生成不可复用的
工作单元实例：

```text
work_unit_instance_id = H("review-work-unit-instance-v1", {
  campaign_id,
  plan_generation,
  task_id,
  task_revision_id
})
```

任何 accepted event 只要推进 `plan_generation`，都必须内嵌统一的
`plan-generation-transition-v1` composite，而不只在 split/merge/delete 时迁移。Payload 至少包含完整
predecessor/successor work-unit map（普通 revision 更新为 1→1）、finding 唯一 owner、task lifecycle、
basis review/reply、continuity ordinal、已结算 debit、active reservation 为零证明和 conserved entitlement
transfer。Predecessor 进入 `awaiting-successor-verification`；successor 继承可继续审核所需的显式事实，
不能靠相同 `task_id`、SQLite 当前行或“由实现推断”迁移。Candidate、evidence、bounded/exact host revision
和 dependency refresh 均使用同一 schema；缺 transition 的 generation event 整体拒绝。

同一 generation 内 `task_id`/`task_revision_id` 组合必须唯一，因此无需非确定 nonce；相同 task 在后续
generation 重新出现会得到新的 work-unit instance。Lineage edge 只允许从 generation `g` 的实例指向
`g+1` 的实例，并在单一 generation composite event 中校验 predecessor/successor coverage、edge
完整性和严格递增，天然不可能形成回边。SQLite 的 task lifecycle、finding owner、round、entitlement
和 CLI 路由均以 `work_unit_instance_id` 为主键；`task_id` 只是内容索引。若 CLI 的 `--task` 在 current
generation 不能唯一解析为一个实例，必须要求显式 `--work-unit`，不能把历史同 ID 实例合并成一行。
`public_path_allowlist` 使用 `/` 分隔的 Git-style 公开仓库相对路径，以原始逻辑路径的 UTF-8 bytes
排序，不做 case-fold 或 Unicode 归一化；无法无歧义 round-trip 或发生规范路径碰撞时失败关闭。两个
`ordered_*_task_revision_ids` 均按 `task_id`、再按 `task_revision_id` 进行字节序排序；重复项直接
拒绝，不能依赖文件系统枚举、SQLite 返回或并发完成顺序。同一 trigger/idempotency key 与相同输入
重新 plan 应得到相同 `campaign_id`；不同触发但相同内容得到不同 campaign、相同
`plan_content_key`。
campaign 一经授权，`campaign_id` 不再改变；每次修复或补充证据后生成新的 `plan_revision_id` 并
写入事件链。任何可审核内容或实际依赖改变都会产生新的 task/plan revision，再由第 6.3 节判断
它是授权派生还是 scope drift，不能静默覆盖初始快照或另起无关联 campaign。

逻辑 allowlist 不是文件读取授权的充分条件。所有 bundle、evidence、canonical revision、candidate
验证、临时副本和测试输入必须通过同一个 `SafePublicFileResolver`：

- 固定公开仓库根的 directory fd；每个中间组件先 `lstat`/等价 no-follow 检查，再相对上一级已验证
  fd 使用 `openat(O_DIRECTORY|O_NOFOLLOW)`/等价原语打开并对该 fd `fstat`，下一组件只相对新 fd
  解析，绝不重新拼接字符串路径。只允许真实目录组件，拒绝 symlink、junction、reparse point、
  mount redirection、device 变化和其他特殊对象；
- 最终文件用 `openat`/等价 no-follow 原语打开，再对同一 fd `fstat`，只接受 `st_nlink==1` 的
  regular file，拒绝可能把仓库外对象硬链接进来的多链接文件；检查与读取必须使用同一 fd，不能
  check 后按字符串路径重开；平台无法可靠提供这些语义时失败关闭；
- 拒绝 Git mode `120000`、submodule/special mode、设备、socket、FIFO；文件 mode/type 进入
  `revision_hash`。Candidate 不得创建 symlink、改变为特殊 type，临时副本也不得保留链接；
- 每个物理 fd 必须由上述 root-anchored fd chain 证明仍位于固定公开仓库根；resolver 不调用
  `realpath` 追随链接，也不 `stat`、枚举或读取 protected root。Protected root 只以不可外发的预声明
  deny policy token 参与失败分类，诊断只保存 component/error category；
- 路径组件、mode 或 inode 在构建 payload 前后变化视为 TOCTOU，立即丢弃快照并失败关闭。

因此即使公开路径 `public/link` 指向受保护 DLC，resolver 也会在读取目标内容之前拒绝。任何证据
提取器、patch 工具或测试 runner 绕过 resolver 都属于边界违规。

### 6.2 状态机

状态分为 finding、task 和 campaign 三层；每层都只有 event 驱动的规范转换，不能靠 SQLite 更新或
“没有待办”推断。

Task 使用以下主路径；本地 cache、外发、candidate、宿主修订和 evidence 是显式分支：

```text
planned
  → cache-checking ── clean cache ──────────────→ verified
       ├─ cache with findings ──────────────────→ reviewed
       └─ miss/fresh-required → awaiting-external-authorization
                                 → authorized → running → reviewed
                                                            ├─ clean → verified
                                                            ├─ candidate-validated
                                                            │   → candidate-accepted → applied
                                                            │   → codex-response-recorded
                                                            │   → re-review-required → cache-checking
                                                            ├─ remediation-required → remediation-planned
                                                            │   → remediation-running → remediation-result-validated
                                                            │       ├─ candidate → candidate-validated
                                                            │       └─ advice/no-change → host-action-required
                                                            ├─ bounded-host-revision-accepted
                                                            │   → codex-response-recorded
                                                            │   → re-review-required → cache-checking
                                                            ├─ exact-host-revision-authorized-and-accepted
                                                            │   → codex-response-recorded
                                                            │   → re-review-required → cache-checking
                                                            ├─ evidence-validated → evidence-accepted
                                                            │   → codex-response-recorded
                                                            │   → re-review-required → cache-checking
                                                            └─ codex-response-recorded
                                                                → re-review-required → cache-checking

task-lineage-replaced → awaiting-successor-verification
  → task-verified-via-successors

任意非 terminal 状态 → termination-requested → draining
  → task-waived | task-escalated | task-failed | task-cancelled | task-superseded
```

Task 状态描述执行进度；finding 的逐项状态由第 12 节 ledger 管理。`codex-response-recorded` 只说明
答复 artifact 已通过本地合同校验，不表示 Pi 已接受答复。Pi 的 `resolved` 也不能直接令 task
verified；宿主仍须核对 revision、本地测试和第 13.4 节独立复审 gate。

Candidate 主路径的顺序是强约束：`candidate-validated` 只说明临时副本校验通过；主代理必须再通过
`candidate-generation-accepted` 把规范 group 集推进到 `candidate-accepted`，真实工作区精确匹配后
才能 `record-applied`。应用产生 current revision 后，`audit respond` 才能以 `fixed` 绑定实际变化，
随后进入 re-review。`record-applied` 不得接受只有 `candidate-validated` 而没有 accepted generation
的 group，也不得把应用前 reply 移植到应用后 revision。没有 candidate 的人工修订在 bounded 模式走
`bounded-host-revision-accepted`，在默认 exact 模式走绑定完整 reauthorization 的
`exact-host-revision-authorized-and-accepted`；纯反驳可直接记录 reply，但都必须在同一 task terminal
前复核。额外 remediation 只负责产生绑定 finding 的候选或 advice，不直接关闭 finding。

Task terminal 分两类。成功 terminal 为 `verified`、有效 `task-waived` 和
`task-verified-via-successors`；非成功 terminal 为 `task-escalated`、`task-failed`、`task-cancelled`
和 `task-superseded`。精确 cache hit 在 target campaign 通过本地 scope/alias/validator/completion
gate 后提交 `task-verified-from-cache` 直接转换到 `verified`，不要求外部转移 authorization；cache
result 含 finding 时只能原子物化到 `reviewed`/ledger，不能提交该成功转换。Cache event 本身不是
task terminal。非成功 terminal 不会让 finding 看似关闭，但会让旧 campaign 可确定
停止并把后续责任绑定到 follow-up、replacement 或人工决定。

Planner split、merge 或派生删除不能把 predecessor 直接标为非成功 `task-superseded` 后再要求
campaign “全部成功”。`task-lineage-replaced` 必须在一个 generation event 中保存 predecessor/successor
`work_unit_instance_id` 集、每个 item/revision 的覆盖映射、finding 唯一迁移映射、conserved entitlement
allocation 和删除验证实例；每条 edge 必须从 `g` 严格指向 `g+1`，并在 commit 前执行 acyclic/coverage
校验。Predecessor 先进入 `awaiting-successor-verification`；只有所有 successor 均为成功 terminal、
迁移 finding 已有有效 disposition，且 successor item 并集或受审核的删除 diff 与 predecessor 覆盖
精确相等，才能提交 `task-verified-via-successors`。Merge 可让多个 predecessor 指向同一 successor；
delete 必须至少指向一个包含公开删除 diff 的 verification work-unit，不能使用空 successor 集声称成功。

动态 regrouping 默认只允许 history-equivalent work-unit：stage、下一 continuity ordinal、basis review、
reply/evidence generation、final/remediation 状态及可用 entitlement 的语义必须兼容。异构历史 task 不得
merge；已消耗轮次的 task 也不得 split 后让多个 successor 各自取得同一下一 ordinal。若未来需要支持
异构 regrouping，必须先引入 per-lineage history vector 和逐 pool 的 request debit；MVP 固定 packing，
完全不进入该分支。

Continuity、independent-final、remediation、payload-repair、force 和其他 stage request 使用 lineage-scoped
conserved entitlement，而不是“每个新 task 重新获得上限”。每个初始 work-unit 得到不可变
`entitlement_pool_id = H("lineage-entitlement-pool-v1", {campaign_id,
root_work_unit_instance_id})`；authorization revision 只向该稳定 pool 分配上限，不改变 pool identity。
Split 后所有 successor 共享同一剩余 pool，或由 generation event 显式分配其
未消费份额，分配总和不得大于 predecessor remaining。Merge 只合并不同 pool 的剩余额度并按 pool ID
去重，不能把共同祖先重复相加。每个新 request 必须在 campaign lock 下从明确 pool 原子 reservation，
terminal/取消规则决定消耗或返还，不能仅把 `used=2` 复制给两个 successor 后让它们各运行 ordinal 3。

Planner 每次 lineage 改变都必须基于 current work-unit instances、共享/分配后的 entitlement、retry/
repair/force 和 remediation/final 分支重新冻结 stage graph 与 `max_reachable_calls`。若完成所有 successor
所需额度超过 conserved remaining 或当前累计 authorization ceiling，generation 先进入
`awaiting-plan-reauthorization`，不得激活 successor/provider attempt；用户批准完整新 authorization 后，
单一 generation event 才可增加明确的 pool entitlement。全局 call ceiling 只是最后一道 gate，不能让
已承诺路径运行到中途才发现不可达。

Campaign 使用规范状态：

```text
planned → local-evaluation ── empty/cache-only ──→ completed-verified
              └─ miss/fresh-required → awaiting-external-authorization
                                        → authorized → running → completed-verified

任意非 terminal 状态 → termination-requested → draining
  → terminated-escalated | terminated-failed | terminated-cancelled | superseded
```

`completed-verified` 是唯一成功完成状态。`terminated-*`/`superseded` 是不可变非成功终态：报告必须
保留 open/escalated findings、原因、责任人/授权记录和可选 successor campaign，不能宣称审核通过。
Successor 只能通过第 6.1 节新的 `campaign-requested` trigger 创建并引用旧 campaign；不能重新打开
旧 state。Terminal 之后 event chain 只允许白名单中的 state-neutral 审计事实（例如去敏 late response
或 settlement incident reference），不得新增 task/finding、改变 completion/disposition 或恢复运行。

任何 task/campaign terminal event 提交前都必须通过 drain barrier：不存在 active attempt/reservation、
pending/active provider slot、active cache flight、`classified-pending-target`、
`awaiting-cache-resolution`、`abandon-pending`、未结算 transport retry/remediation、正在进行的
independent-final instance 或未完成的 lineage/entitlement transfer。终止请求先禁止新
plan/request/attempt；所有 attempt/transfer/request 组合严格按第 8.1 节穷举 reducer 关闭。Crash recovery
从 event chain 继续 draining，并被明确授权补提该表中的唯一 pre-transfer cancel、post-transfer abandon、
pending target/slot/flight 收尾和 outer terminal。若无 active work，`termination-requested` 与目标 terminal
可在同一锁事务的相邻事件中完成；绝不能先把外层对象 terminal，再留下只能靠 terminal 后例外事件
结算的 reservation、round 或全局资源 slot。

Campaign 非成功 terminal 的 drain barrier 还要求所有 current/historical child work-unit 已有规范 terminal。
`campaign-termination-requested` 必须按确定性 child cascade 为每个 planned/reviewed/awaiting-* child 记录
对应 task cancellation/escalation/failure、未关闭 finding 和 follow-up responsibility；不得只因 active
attempt/resource 为空就先 terminalize outer campaign。Mixed verified/planned/reviewed/escalated child 的
结果由冻结表唯一决定，恢复器逐项幂等补提，最后才提交 outer terminal。

Campaign 只有同时满足以下条件才能进入 `completed-verified`：

- 当前 generation 的所有 work-unit instances 均为 `verified` 或未过期的 `task-waived`；历史 predecessor 均为
  `task-verified-via-successors`，cache result 必须先按上文转换为 `verified`；
- 所有 finding 均有明确 disposition；
- 所有已应用修订通过对应的本地检查；
- 所有受影响 task 已重新审核；
- 初始 task 即使后来重分包或消失，也存在可追溯的 lineage-success terminal，而不是从集合中静默删除；
- 没有未处理的 scope drift，且 current generation 不存在 campaign local logical scope 或 accepted
  candidate/evidence/host-revision/dependency chain 之外的新增文件/task revision；发生过外发时还必须
  满足 current external authorization；
- drain barrier 为空，且不存在 unresolved cache conflict、stale cache-classification token 或
  `awaiting-terminal-disposition`。

零 task 计划使用显式的 empty-plan 完成规则：`plan-generation-created` 必须证明输入 scope 成功解析、
planner/本地检查均成功、task count 为 0，且 purpose policy 允许“无可审内容”；随后
`campaign-completed-verified` 记录 `completion_kind=empty-plan`。提取失败、输入缺失、被策略意外过滤
或全量任务期望与零计数矛盾时不能走 empty-plan。Cache-only campaign 则逐 task 提交
`task-verified-from-cache` 后以 `completion_kind=cache-only` 完成。

控制事件至少包括：`task-verified-from-cache`、`candidate-generation-accepted`、
`bounded-host-revision-accepted`、`exact-host-revision-authorized-and-accepted`、
`remediation-planned`、`remediation-result-validated`、`evidence-supplement-accepted`、`task-lineage-replaced`、
`task-verified-via-successors`、`task-termination-requested`、`campaign-termination-requested`、
`task-waived`、`task-escalated`、`task-failed`、`task-cancelled`、`task-superseded`、
`campaign-completed-verified`、`campaign-terminated-escalated`、`campaign-terminated-failed`、
`campaign-terminated-cancelled` 和 `campaign-superseded`。每个事件必须列出受影响 finding refs、reason、
approver/authority、当前 revision、drain snapshot 和 successor（如有）。不允许以删除 task/finding、
批量改 disposition、超时或 SQLite 当前行自动推导 terminal。

### 6.3 授权记录

Campaign 把本地处理 policy 与外部转移 authorization 分开。`campaign-policy-bound` 在 genesis/plan
阶段冻结 planner、SafePublicFileResolver、cache-use、validator、redaction 和 completion policy；它
允许读取当前公开 allowlist、构建本地 bundle、查询/重验本地 cache 和完成 empty/cache-only campaign，
但绝不允许 provider 调用。只有 review/remediation cache miss、`--force` 或 fresh-only 独立终审准备外发时，才需要下述
不可变 external-transfer authorization。来源 campaign 的授权既不需要、也不能被目标 cache hit 继承。
本地 policy 同时冻结 plan logical scope 和 local bundle/count caps；后续 external authorization 必须
明确重述其准备外发的子集与更严格或相等的 caps，不能借“本地已经读取”把更大范围自动外发。

外部转移授权是 campaign 的显式对象，至少记录：

- `authorization_id`、`parent_authorization_id_or_null`、campaign ID、revision ordinal 和完整对象 digest；
- 允许的 provider、model、thinking 集合，以及每个模型别名的 mapping digest、provider-qualified
  immutable model/deployment identity 和规范 `model_lineage_id`；
- campaign、provider/deployment pool 及 `bundle_kind × risk_class` 的 authoritative active-attempt cap；
  默认公开低风险代码为 2，翻译或 high-risk/security 为 1，多个适用 cap 取最小值；
- bundle kind；
- 公开文件白名单；
- 初始授权 work-unit/task 集合、每个 task 的 base revision 及其 `entitlement_pool_id`；
- 逻辑 item scope digest、每 generation 最大 current bundle 数、campaign 最大唯一 outbound bundle 数；
- revision 授权模式：默认 `exact-candidate-only`，或用户明确批准的
  `bounded-same-logical-scope`；后者还必须给出 host revision generation、累计 outbound bytes、
  单 generation diff bytes/hunk/file 数、必须绑定的 finding/reply 和允许的 validator/redaction policy
  上限；
- campaign 累计绝对上限：外部调用、输入/输出 token 和可选费用；每个维度的
  `hard|forecast|disabled` mode 与上界证明；
- 若启用费用预算，冻结的 provider price quote 或版本化 price-table snapshot、币种和保守计价策略；
- 允许的阶段枚举：`initial-review`、`review-reply`、`evidence-supplement`、`payload-repair`、
  `remediation`、`final-review`；除初审外每类调用都必须显式授权，`payload-repair` 不得携带新证据；
- 各阶段独立 call 上限，以及 `allow_payload_repair` 与每个 review request 最多一次的
  `max_payload_repairs`、每个冻结 request 的 `max_transport_attempts`（默认 2，严格串行），以及每个
  result key 的 `max_forced_observations`（最多 1）和 campaign
  `max_forced_observations_total`（普通 campaign 默认 0，周期复检/manual-rerun 显式授权）；
- 每个初始 work-unit lineage 的 `max_continuity_rounds`（默认 3）、每 ordinal 最大 pre-transfer replan instances、
  `max_independent_final_reviews`（默认 1）、每 lineage 的 `max_remediation_requests`（默认 1）和 campaign
  总 review/call 上限；这些限制以第 6.2 节 `entitlement_pool_id` 冻结并守恒，不能在 split/merge 后按
  successor 复制。Continuity、remediation 与独立终审分开计数，同一冻结 request 可有多个串行
  transport attempt 但只能接受一个 validated result，旧 revision 的晚到答复标记 stale；
- 由上述 stage/retry/repair 上限推导的 `minimum_calls`、`expected_calls` 和
  `max_reachable_calls`，以及按 active lineage pool 逐项列出的 entitlement allocation；每次 plan
  generation/split/merge/remediation 分支变化都必须重算，`max_reachable_calls` 不得大于 campaign hard
  call ceiling；
- 允许的证据 request kind、独立复审模型和候选应用策略；
- 授权时间和可选失效时间；
- 用户可读的范围摘要。

`authorization_id = H("campaign-authorization-v3", authorization_body_without_id)`；body 包含上述完整
字段、revision ordinal、parent 和 authority confirmation digest，不能把 ID 自身放回 body 形成循环。

Campaign 首次向外部 provider 转移 payload 前，CLI 必须向用户明确展示 provider、alias、resolved
deployment identity 与 underlying model lineage、bundle kind、task/item/bundle 数、revision 授权模式、
最短/预计/最坏可达调用数和各预算 mode/ceiling，并把用户确认摘要纳入 authority object；项目级
全局网络放行或来源 campaign 的 authorization 不能替代该确认。普通 cache hit 不发生外部转移，
因此既不替代确认，也不触发确认；若随后出现 miss，task 必须停在
`awaiting-external-authorization`，取得本 campaign 的确认后才能创建 attempt。

授权对象必须保存为不可变、完整快照。初始授权通过 `campaign-authorized`，后续通过
`campaign-reauthorized` event 记录 parent/current object digest、用户确认摘要、集合/上限 diff 和
生效 plan revision；SQLite 只投影 current authorization 与 remaining budget。每个 attempt 永久绑定
它实际使用的 authorization revision。

Reauthorization 不使用“新增额度”或局部 patch：新 revision 重述完整 scope/model/stage/cumulative
ceilings，并以 `parent_authorization_id` 形成单链。Cumulative ceiling 是 campaign 自创建以来的绝对
上限，不能因 reauthorize/resume/new run 清零；新 ceiling 不得小于“所有 finalized debit + active
reservations”，降低 scope 也不能抹掉历史外发。扩展 provider/model/path/stage、提高上限或改变
hard/forecast mode、alias mapping digest、resolved deployment 或 model lineage 都必须取得对应的新
用户授权；集合替换/扩展语义由完整新快照唯一决定。删除
SQLite 后只重放 authorization objects/events 即可得到同一 current revision 与 remaining。

预算分为两个作用域，不能用同一个计数器混合：

- plan-scoped hard limits：campaign local policy 的逻辑 item/path/kind scope、
  `max_current_bundles_per_generation` 和
  `max_unique_outbound_bundles_per_campaign`。每个 `plan-generation-created` event 固化 generation、
  current task/bundle revision set、来源和 canonical count；candidate 派生只接受
  `candidate-generation-accepted` 因果链，补证只接受已授权 `evidence-supplement-accepted` event，
  有界人工修订只接受 `bounded-host-revision-accepted`，默认 exact 模式的 byte-different 人工修订只
  接受与完整 reauthorization 合并的 `exact-host-revision-authorized-and-accepted`。
  在原逻辑 scope 内产生有 accepted event 的新 revision 是正常派生，不算新增 item；超出逻辑
  item/path/kind 才是 drift。真正外发时还必须落在 current external authorization 重述的 scope/caps 内。
  若 deterministic planner 因大小变化拆分/合并同一 logical items，generation event 必须携带完整
  predecessor→successor work-unit lineage、finding owner mapping、已用 debit 和第 6.2 节守恒的 entitlement
  pool/allocation；缺 lineage、复用历史 instance identity、形成非递增 edge 或试图借 regrouping 复制/
  重置轮次与额度时按 drift 处理。
  Current bundle cap 每代重算，unique outbound cap 只在某个 semantic payload 首次外发时累计；retry、
  cache hit 和同 payload attempt 不重复消耗 unique bundle；
- attempt-scoped dimensions：`calls` 始终 hard；`input_tokens`、`output_tokens`、`cost` 各自为
  `hard`、`forecast` 或 `disabled`。Hard 进入下面的 reservation/settlement reducer；forecast 只用于
  planning/报告，不是授权边界，不能在 UI 或完成报告中称作硬上限。

Remaining hard attempt budget 只能由授权对象和 event chain 重建，不能读取 SQLite 中的累计值作为
事实来源。对每个 hard 维度 `d ∈ {calls, input_tokens, output_tokens, cost}`，使用同一版本化算法：

```text
remaining[d] = authorized[d] - sum(effective_debit(attempt, d))
```

每个 attempt 的 `effective_debit` 按状态确定：

- active attempt：使用 `attempt-started` 中的 reservation；
- validated/failed/stale completion：calls 对存在 `external-transfer-started` 的已计费或可能外发 attempt
  计 1，token/cost 有 provider actual 时
  只有当 raw usage 覆盖 hard contract 声明的全部计费类别并通过校验时才使用 actual，否则保留
  reservation；不得同时累加 reservation 与 actual；
- lease expired 且不能证明尚未外发：按 reservation 保守结算，晚到 actual 只允许增加 debit；
- 只有 event chain 能证明该 request 的对应 attempt 从未出现 `external-transfer-started`，并提交
  `attempt-failed-before-transfer`、`attempt-lease-expired-before-transfer` 或第 8.1 节 composite
  pre-transfer cancellation 时才释放 reservation；进程消失但 lease 尚未 canonical terminal、usage
  缺失或 transfer 状态未知不能释放；
- transport retry、`--force`、payload repair 和 final review 的每次外发都是独立 attempt，各自预留并
  结算；它们的语义 generation/continuity 归属按第 9.3、13.3、13.4 节另行计算。

Hard token reservation 不能使用历史 p90。Input 使用 provider/token-accounting contract 认可的精确
tokenizer 或证明不低于真实计费量的 deterministic upper bound；output 使用 provider 强制执行的
`max_output_tokens`，并覆盖 reasoning/cached/tool 等该 provider 可能计费的全部类别。无法证明上界时
该维度只能显式设为 forecast，或在外发前失败关闭。若 provider actual 超过已冻结的 certified hard
bound，提交 `budget-integrity-failure`、请求 `terminated-failed` 并按 drain barrier 结算后终止 campaign，
同时报告潜在授权越界，不能把它当作普通
`budget-overrun` 后继续。

`cost` disabled 时 usage 可以为 `null`；forecast 时记录估算/actual 但不称为授权 ceiling；hard 时
每个 attempt 必须使用冻结 provider quote/price table 和上述 hard token upper bounds 计算最坏情况、
非空、同币种的 reservation。无法取得可信价格、币种不匹配或上限无法数值比较时，在
`attempt-started` 前失败关闭。Provider actual 不可用时保留 hard reservation；actual 大于 certified
cost upper bound 视为 `budget-integrity-failure`，而非可接受的事后超限。

Validated result composite 内的 `attempt_terminal`、`attempt-failed`、`attempt-stale`、
`attempt-lease-expired` 及所有明确的 pre-transfer terminal 都必须引用原 reservation digest，并记录
settlement/delta。
恢复时逐 attempt 归约这些事件；重复 terminal event、负 debit、actual 小于零、超出授权币种或
无法唯一匹配 reservation 时失败关闭。SQLite 重建后得到的 remaining 必须与未删除前逐维一致。

Revision 授权有两种不可混用的模式：

- `exact-candidate-only`：自动派生只允许初始 snapshot、精确 accepted candidate、accepted evidence 和
  版本化 dependency refresh；其他字节变化不会自动进入 plan chain，只能由下文一次性、精确 snapshot
  绑定的 `exact-host-revision-authorized-and-accepted` composite 显式重新授权并接受。这是未明示选择
  时的安全默认。
- `bounded-same-logical-scope`：用户在首次确认时明确允许主代理围绕当前 finding 修改既有 allowlist
  内的同一 logical item/path，并在冻结的 generation/bytes/files/hunks/unique-payload/call/token/cost
  上限内再次外发。它不允许新 item/path/kind、未绑定的顺手修复、特殊文件、secret/redaction policy
  失败或任何受保护输入；任一上限/集合变化仍须 reauthorize。

效率推荐是：对明确包含“审核后修复”目的的低风险公开代码 campaign，授权 UI 首选展示
`bounded-same-logical-scope` 方案及 planner 推导的保守 caps，用户一次确认后正常 host fix 不再重复
确认；对 security/blocker、翻译规范文件、无法证明 caps 的场景，以及用户未明确选择时，使用
`exact-candidate-only`。这里的“推荐”是可见选项，不是静默扩大授权。

精确 candidate 使用第 13.2 节定义的原子 group；每个 group 绑定一个 `base_plan_revision_id`。对授权
初始内容快照 `S0` 及其 plan revision `P0`，逐代计算：

```text
Cg = canonical_sort(
  accepted_candidate_groups where base_plan_revision_id == Pg,
  key = (primary_finding_key, candidate_group_digest)
)

S(g+1) = apply_atomic(Sg, Cg)
P(g+1) = H("plan-revision-v2", {
  campaign_id,
  plan_generation: g+1,
  ordered_current_task_revision_ids(S(g+1)),
  dependency_digest(S(g+1))
})
```

`primary_finding_key` 是 group 所绑定 finding keys 的规范最小值。排序使用规范 UTF-8 bytes，
不得使用接受时间、SQLite 行顺序、模型输出顺序或并发完成顺序。accepted event 中的 group 列表
必须已经处于规范顺序；乱序、重复、缺项、额外项或 base generation 断链均拒绝，不能在重放时
静默重排修复。不同 generation 的先后只由 `base_plan_revision_id → P(g+1)` 因果链决定。

每代以 `candidate-generation-accepted` event 固化 base plan revision、完整有序 group digests、
期望 per-file/task revision set 和 `P(g+1)`；恢复时从对象重新 apply 并比对这些字段。只有单独的
candidate accepted event、却未进入 generation event 的 group 不属于派生链。

在 `exact-candidate-only` 下，唯一可运行判定仍是 canonical 内容：只有工作区实际 revision set 与
`S(g+1)` 的期望 revision set 完全一致、路径仍在原白名单、所有 candidate group 均来自预先记录的
授权链且未超过阶段和预算限制时，才可复用外发授权。系统不判断这些字节由 patch 工具还是人工
键入；主代理精确复现 accepted group 的同一 canonical bytes 可以通过，但 accepted generation 和
应用事件必须早已存在。语义相近但 canonical bytes 不同的人工改写、formatter 额外字节、候选之外
hunk、新文件或未绑定 finding 的顺手修复都不属于 exact 派生。

默认 exact 模式下没有 candidate 的 host fix 仍然可达，但每个 byte-different snapshot 都需要一次
显式 authority。`exact-host-revision-authorized-and-accepted` 是单一 campaign composite event，必须
同时内嵌：current parent authorization（campaign 尚无外发 authorization 时为 `null`）、用户确认过的
完整新 authorization snapshot、base/new plan
revision、逐 file/item exact canonical revision 与 diff digest、当前 finding bindings、
SafePublicFileResolver/secret/redaction/local-test proof、expected next generation 和累计预算/call
预览。它在一个 event 中同时产生 `campaign-authorized|campaign-reauthorized` 与 plan-scoped exact host
acceptance 两个子事实，避免“已经获准外发却仍不在 accepted plan chain”或反向半状态；任何一项失败
均零状态变化。无 parent 时必须满足首次 authorization 的全部展示/确认规则，不能伪造 parent。

该 composite 只接受当前公开 logical scope 内已经由主代理产生的精确 bytes，不是候选生成授权、
不允许未来任意修改，也不表示修复语义正确。提交后仍必须记录 current-revision reply、运行只读
验证并按风险进入 continuity/final review。新 path/item/kind、未绑定 finding、special file、受保护
输入或无法通过 redaction 的内容不能借该 event 进入；它们继续按 scope expansion/new campaign 处理。
若高风险修订没有 conserved independent-final entitlement 或完整预算，composite 在用户确认前就必须
拒绝并给出新的完整授权预览。

在 `bounded-same-logical-scope` 下，byte-different 人工修订先生成新的本地 plan generation，并由
`bounded-host-revision-accepted` 原子记录 base/new plan revision、逐 item/file canonical diff digest、绑定的
finding/reply、authority、SafePublicFileResolver 证明、secret/redaction/size/hunk/file gate、累计
host generation 与 outbound caps。该 event 只表示修订进入已明示的授权派生集合，不代表已审核或
允许自动写工作区；应用后仍须当前 revision reply、本地测试和复审。缺 event、超 cap、无法绑定
当前 finding、加入新 logical scope 或 gate 失败时暂停，必须 reauthorize 或创建新 campaign。

以下变化同样必须重新授权：

- 新增公开文件或扩大翻译组件范围；
- 加入此前未外发的内容类型；
- 使用授权集合之外的 provider/model/thinking；
- 从 `exact-candidate-only` 改为 `bounded-same-logical-scope`，或提高后者任何 generation/bytes/file/hunk
  上限；
- 超过批准的条目、bundle、调用、token 或费用数量。

受保护输入是不可授权的硬边界：相关请求必须直接拒绝，不能通过重新授权或扩大 campaign
转为可发送内容。

缓存命中不产生新的外发，但仍须重新验证当前 campaign 的公开白名单、bundle kind、task revision、
本地 cache-use/completion policy 和可接受 model lineage。它不要求 external-transfer authorization，
也不能从 source 继承该授权。当前 campaign 必须自行生成并验证本地 `bundle_digest` 和 alias mapping；只有其
模型语义投影得到与旧结果相同的 `result_cache_key` 时，才能按第 8.2 节重新物化 target envelope。
Source/target 的本地 bundle digest、campaign ID 和 `finding_ref` 可以不同。Cache hit 由单一
`review-round-validated(source=cache)` event 原子记录 `cache_attachment`（来源 campaign/result、目标
bundle/key、重验证证明）、当前 ref allocation 和完整 ledger delta，不能先 attach 再逐项提交；也不能
沿用来源 campaign 的 scope、外发授权或 disposition event。

Scope drift 使用可操作的 generation 集合差定义：每次执行、补证、应用候选和 cache attach 前，
把当前 plan generation 的 item/path/kind 与 campaign local logical scope 比较；若即将外发，再与
current external authorization 的 outbound scope/caps 比较。随后把 current revision/dependency/
evidence set 与 event chain 中的 `plan-generation-created`、`candidate-generation-accepted`、
`bounded-host-revision-accepted`、`exact-host-revision-authorized-and-accepted` 和
`evidence-supplement-accepted` 因果链比较。原逻辑 item 的精确候选 revision、有界/一次性 exact host
revision、已授权 dependency refresh 或有界补证只有在对应 accepted event 已
提交后才属于当前 generation；它们不扩大逻辑 scope，
但会产生新的 local bundle。出现无 predecessor lineage 的新 task、新 item/path/kind、未获准
dependency/evidence、无法绑定 accepted chain 的 revision 或 generation 断代即为 drift，并暂停外发。

任务消失不能默认当作无害 scope 收缩。只有当消失是 accepted candidate、已明示允许的 bounded
host revision 或精确授权并接受的 exact host revision 的受控派生结果，且删除/替换本身仍作为公开 deletion-verification successor work-unit 通过
最终复审时，才能提交 `scope-contraction-accepted` event；predecessor 随后按第 6.2 节进入
`task-verified-via-successors`，其 finding 以 lineage disposition 关闭，reason 固定为
`authorized-derived-removal`，同时绑定 candidate/host revision、旧/新 plan revision 和最终复审结果。
不对应 accepted generation 的人工删除、
命令行缩小 scope、planner 漏项、
输入缺失或其他无法绑定候选的消失都属于 drift；若用户明确决定缩小范围，应终止或 supersede
旧 campaign、记录原因并为新范围重新 plan/授权，不能把旧 finding 伪装成已验证完成。

## 7. 稳定身份与精确失效

### 7.1 Item identity 与 revision 分离

模型看到短别名，本地系统保存稳定身份和内容版本：

```json
{
  "alias": "i03",
  "item_id": "stable logical identity",
  "revision_hash": "hash of current reviewable content"
}
```

翻译 `item_id` 不包含 target 或全局 ordinal。逻辑身份应由 component、section、source、
source_tag 和局部 occurrence anchor 构成；target、args_order、special 等规范字段进入
`revision_hash`。行号只作为诊断元数据，不参与身份或 revision。完全相同的重复项可形成
occurrence group，并保留成员映射。group 内每个成员必须有不依赖全局 ordinal/行号的稳定
`member_anchor`；member 级 finding 的 evidence 必须绑定该 anchor，只有明确作用于全组时才允许
使用 `group:*`。

代码 item 的身份由公开相对路径和稳定 symbol/hunk anchor 构成，diff 正文进入
`revision_hash`。路径重命名作为显式迁移事件处理。

```text
translation_item_id = H("translation-item-v2", {
  component, section, source, source_tag, occurrence_anchor
})

code_item_id = H("code-item-v2", {
  canonical_public_relative_path, stable_symbol_or_hunk_anchor
})

revision_hash = H("item-revision-v2", {
  revision_canonicalization_version, item_kind, file_mode_and_type_or_null, canonical_revision_bytes
})
```

`revision_hash` 必须在任何 outbound redaction 之前，由未脱敏的规范内容计算。采用带版本的
确定性序列化 `revision-canonical-v1`：字符串使用 UTF-8，换行统一为 LF，对象键按规范顺序；
除换行外不折叠空格、不改写 literal、不替换绝对路径文本，也不做可能改变语义的 Unicode
归一化。环境中的仓库根路径不进入身份，文件位置使用未脱敏的公开仓库相对路径。

- 翻译 revision 至少包含 component、section、source、target、source_tag、args_order、special、
  occurrence group 及该条目实际使用的规范字段；
- 代码 revision 至少包含公开相对路径、文件状态、稳定 anchor 和完整未脱敏 diff/hunk 字节；
- 依赖摘要另行计算并进入 `task_revision_id`，不能用 redacted payload 代替规范 revision；
- canonicalization 规则变化必须提升 `revision_canonicalization_version`，令旧结果精确失效。

本方案选择严格 formatter 语义：`expected == actual` 比较的是上述 canonical bytes，只允许
`revision-canonical-v1` 已声明的 UTF-8/LF 规范化，不运行 formatter、pretty-printer 或 lint
autofix。候选应用环境必须关闭 format-on-save 和修改型 hook；lint、测试和 validator 默认只读。
在 accepted candidate group 产生的 expected snapshot 之外，任何工具或人工操作只要进一步改变
canonical 内容，即使自称“仅格式化”，都不再属于 candidate 派生；在尚无独立
`bounded-host-revision-accepted` 或 `exact-host-revision-authorized-and-accepted` 时按 scope drift 处理。
确需格式化时，把格式化后的内容作为新 plan 输入，按第 6.3 节 bounded mode 接受或以一次性 exact
composite 重新授权并接受；未来若引入格式化
归一化，必须提升 canonicalization 版本并重新做非单射与语义保持验证。

外发时另行计算
`payload_digest = H("outbound-semantic-payload-v2", exact_outbound_redacted_bytes)`，并记录
`redaction_version`。`revision_hash` 证明本地语义输入，`payload_digest` 证明实际传输内容；第 8.2 节
的 semantic context/cache key 必须同时绑定两者。这样不同未脱敏内容即使 redaction 后文本相同，也
不会错误复用结果。

### 7.2 细粒度依赖摘要

Bundle 只绑定实际使用的依赖：

- 代码 bundle：公开 diff revision、相关策略摘要、redaction 版本；
- 翻译 bundle：条目 revision、相关术语行摘要、格式/标记策略摘要；
- 不再绑定完整 manifest 原始字节。

无关 manifest 或组件变化不应令代码 bundle、其他组件翻译 bundle 失效。

## 8. 内容寻址存储与执行缓存

### 8.1 存储布局

建议使用不可变 JSON 对象、每 campaign 的 append-only event chain，以及可重建的 SQLite
投影：

```text
.artifacts/i18n/
  objects/sha256/<prefix>/<digest>.json
  executions/<result-cache-key>/observations/<validated-result-digest>.json
  campaigns/<campaign-id>/
    events/<sequence>-<event-id>.json
    events/.pending/<sequence>-<event-id>-<writer-token>-<nonce>.tmp
    events/.aborted-pending/<sequence>-<event-id>-<nonce>.tmp
    work-units/<work-unit-instance-id>/rounds/<continuity-ordinal>/<instance-generation>/requests/<repair-generation>/index.json
    work-units/<work-unit-instance-id>/remediations/<generation>/requests/<repair-generation>/index.json
    work-units/<work-unit-instance-id>/finals/<generation>/requests/<repair-generation>/index.json
    head.json
    campaign.json
  maintenance/events/<sequence>-<event-id>.json
  maintenance/events/.pending/<sequence>-<event-id>-<writer-token>-<nonce>.tmp
  maintenance/events/.aborted-pending/<sequence>-<event-id>-<nonce>.tmp
  locks/cas-reference.lock
  locks/cache-keys/<prefix>/<result-cache-key>.lock
  locks/provider-slots/<prefix>/<provider-pool-key>.lock
  locks/<campaign-id>.lock
  locks/maintenance.lock
  state.sqlite3
```

- JSON 对象保存 bundle、validated review、Codex reply、round disposition、finding 和候选修订。
- 不可变、带 checksum 的 event chain 是 task 状态和因果顺序的唯一事实来源；每个 event 包含
  单调 `sequence`、`event_id`、`parent_event_id`、`scope_kind`、可选 `task_id`/`attempt_id` 和 revision
  绑定。`scope_kind=task` 时 `work_unit_instance_id` 与 `task_id` 都必填；campaign/authorization/writer
  级事件固定 `scope_kind=campaign, work_unit_instance_id=null, task_id=null`，不能伪造占位 task。
- Maintenance chain event 固定 `scope_kind=maintenance`、`campaign_id=null`、
  `work_unit_instance_id=null`、`task_id=null`；其 payload
  可引用 target campaign/request digest，但不能冒充 campaign chain state。
- `state.sqlite3` 只保存可从 event 重建的状态投影、对象引用、调度索引和 lease；使用 WAL，
  但不得把只有 SQLite 中存在的状态当作已提交事实。
- `head.json` 和 `campaign.json` 都是可重建索引/导出，不是事实来源。
- `work-units/*/{rounds,remediations,finals}/**/index.json` 是面向人和 CLI 的派生视图，只引用 CAS 中的 current bundle、prior review、
  Codex reply 和 validated disposition；删除后可由 event chain 重建。
- Artifact 路径不参与内容 ID。
- Artifact root、`events/.pending` 与 `.aborted-pending` 在首个 event 前以 no-follow、owner-only mode 创建，
  验证位于同一文件系统并 fsync 各级父目录；初始化未 durable 时不得发布 genesis。

`event_id = H("campaign-event-v2", {event_schema_version, campaign_id, sequence, parent_event_id,
canonical_event_payload})`；maintenance event 使用对应的 maintenance chain domain。由此可验证顺序、
parent 和 payload 是否被篡改，而 wall-clock 时间只作诊断，不决定因果顺序。

Event 文件本身必须使用与 CAS object 同等级的 crash-atomic 安装协议，不能直接对最终文件名
`open(O_EXCL)` 后边写边暴露。所有 genesis、普通 campaign event、maintenance event、cache/provider
slot event 和 GC progress event 统一执行：

1. 在目标 `events/` 目录同一文件系统的 `.pending/` 中，以不可预测临时名和
   `O_CREAT|O_EXCL|O_NOFOLLOW` 创建 mode `0600` 的 regular file；完整写入 canonical bytes 后检查短写，
   对同一 fd 重新计算 event ID/checksum，并 `fdatasync`/`fsync` 文件；
2. 在仍持有对应锁且重新核对 head、sequence、parent 与 fencing token 后，用可靠的 no-replace
   原子安装把临时 inode 发布为最终 `<sequence>-<event-id>.json`。允许的实现是
   `renameat2(RENAME_NOREPLACE)`、同文件系统 `linkat(temp, final)` 后 unlink temp，或经验证具有相同
   语义的平台原语；不能退回会覆盖已有目标的普通 rename。平台没有可靠 no-replace 原语时失败关闭；
3. `fsync` 最终 `events/` 目录；若使用 hard-link 安装，还要清理临时 link、`fsync .pending/`，并把
   最终文件重新验证为 single-link regular file。完成这些步骤后 event 才向调用方确认 committed，
   provider 才可启动、外层状态才可推进。若在 final link durable 后、temp unlink 前崩溃，recover 可
   证明两名指向同一 inode/digest 后清理 temp，再确认 commit；
4. Pending 名必须预先绑定 chain、sequence、expected event ID、writer token 与 nonce。恢复扫描只把已通过名称、完整长度、checksum、event ID、parent 和目录持久化验证的最终文件视为
   chain 成员，永远忽略 `.pending/`。最终名不存在时，完整且与当前唯一 next event 匹配的 pending
   inode 可在重新取得全部锁后幂等安装；最终名已存在且 bytes/event ID 相同则清理临时文件；最终名
   冲突时失败关闭，不得覆盖。若 pending 名/owner/mode 能证明属于该 chain，但内容截断或 checksum
   无效，则把它 no-replace 移入该 chain 的 `.aborted-pending/`、fsync 目录并保持旧 head，随后允许由
   domain reducer 重新生成 next event；绝不补写原 temp。只有名称/owner/type 异常、无法证明归属或
   quarantine 冲突时才暂停并请求人工处理，不能让正常写入崩溃永久堵死 chain。

崩溃发生在临时创建、部分写入、文件 fsync、no-replace 安装、目录 fsync 或 SQLite projection 的任一
点，都只会得到“旧 head”或“完整新 event”；截断的最终 event 不是允许状态。`.pending/` 只能由上述
恢复器按精确 event digest 清理，不能由通用 GC、按 mtime 猜测或另一个 campaign writer 删除。

每条 campaign chain 的首个 event 必须是 `campaign-created`，`parent_event_id=null`，payload 完整
保存并规范序列化 `plan_content_key`、purpose、parent campaign、`campaign_request_event_digest`、
上游 trigger fact digest、campaign generation、`scope`、公开 allowlist、planner version、policy
digest、ordered initial task revision IDs、相关 schema/canonicalization versions 和对象引用。它是
唯一 genesis 特例：按统一锁序先取得
CAS shared barrier、再取得 OS campaign lock，按上文 pending-write + no-replace install 协议原子 bootstrap
`writer_fencing_token=1`、genesis writer ID、transaction issued/expires 和 `writer_released=true`，
不再先写 `writer-lease-acquired`；`scope_kind=campaign, work_unit_instance_id=null, task_id=null`。Genesis event 成功即关闭这次
短 writer transaction，不把逻辑 lease 留到 provider timeout。恢复时
必须从这些字段重算并匹配
`campaign_id`；缺字段或不匹配即失败关闭。这样删除 `campaign.json` 与 SQLite 后，campaign 身份、
初始范围和任务归属仍能仅由 event chain 重建。

Maintenance chain 对称地以 `maintenance-created` 为首事件，并原子 bootstrap token 1；不存在
SQLite-only maintenance token。仓库第一次 campaign 前先创建/验证 maintenance genesis，再提交
`campaign-requested`；`campaign-created` 必须验证该 request event，但不需要任何先前 campaign-chain
event 或 campaign writer token。已存在 genesis 时，同一 campaign/request 的并发创建者只验证并
复用现有 chain，不能再创建第二 genesis。Genesis transaction 已释放后，下一 writer 可立即通过普通
`writer-lease-acquired` 得到 token 2。

所有写进程使用跨进程 campaign lock 串行提交状态事件，并把“writer lease”和“provider attempt
lease”作为两个不同概念：

- writer lease 是单次 event-commit transaction 的短 lease，记录 `writer_id`、`expires_at` 和单调递增
  的 `fencing_token`；默认 TTL 为版本化 policy 中的 5 秒，绝不能取 provider timeout；
- provider attempt lease 记录 task revision、attempt、provider 调用和独立 expiry；
- 除上述 genesis 外，每个状态 event 必须携带当前 writer `fencing_token`，attempt completion 还必须
  携带 attempt lease token；validated-result composite 内的 terminal 子记录同样必须携带，二者不能
  相互替代。

Provider attempt lease 的 `expires_at` 不得早于
`issued_at + timeout_seconds + completion_commit_grace_seconds`。grace 来自版本化 policy，默认
60 秒，用于 provider 子进程退出、validator 和 completion event 提交；续期只能在原 lease 到期前
提交 `attempt-lease-renewed` event，且不能提高调用或 token 预算。否则一个仍处于允许 timeout 内的
付费响应可能被错误判为 stale。

writer transaction 只在短临界区按统一顺序持有 CAS shared barrier 和 OS advisory lock：读取并验证
event head，以“最近已提交 fencing token + 1”提交 `writer-lease-acquired`，在同一 OS-lock 持有期内
提交一个或一组预先声明的 domain event，最后提交 `writer-lease-released` 并更新 SQLite 投影。
文件级 event chain 不把“一组相邻 event”冒充原子事务：需要全成全败的 disposition、candidate
generation、evidence+plan 或 lineage map 必须编码为一个 composite domain event；多 event 组只能用于
具有显式中间状态和 deterministic recover 的流程（例如 classified-pending-target、abandon-pending 或
termination draining）。
Provider 启动的前置条件不仅是 `attempt-started` 已提交，还包括该 writer release 已提交并释放 OS
lock；因此 provider 调用、1200 秒等待、validator 和用户思考期间都没有逻辑 writer lease。进程退出时
OS lock 由内核释放，也不能通过删除 lock 文件强行解锁。Domain event 只有在 token 等于 event chain
当前 token 且 writer lease 未过期时才接受；旧 writer 即使在暂停或崩溃后复活，其较小 token 也必须
被拒绝，不能通过重写 SQLite 或复用旧 event 获得提交权。

Genesis 之后，`writer-lease-acquired` 是唯一允许携带“当前 token + 1”的特殊 transition，并且只能在 OS lock
内、以已验证 head 为 parent 提交；普通 event 只能携带当前 token。这样 token 提升本身也属于
event 事实，而不是 SQLite 中不可恢复的计数器。

当前短 writer lease 未过期且属于其他 writer 时，新 writer 必须等待或失败，不能抢占；同一 writer
只可在仍持有 OS lock 的长本地 fsync transaction 中用当前 token 续期，禁止为外部调用续期。主动
结束提交 `writer-lease-released`。若进程在 domain event 后、release 前崩溃，其他 writer 最多等待
短 TTL，随后以更大 token 提交 `writer-lease-expired` 并从已提交 head 恢复；这是一项有上界的本地
恢复延迟，不得退化为 1200 秒。复活进程若要继续，必须作为新 writer 获取新 token 并重新验证状态；
用旧 token 预先生成的 event 永远不能重新盖章提交。

默认并发 2 的含义是两个不同 work-unit/key 的 provider 子进程可以重叠运行：worker A 提交并释放
`attempt-started` writer transaction 后等待 provider；worker B 随即可取得更大 writer token、提交
自己的 attempt 并同时外发。若实现把 writer lease 保持到 provider completion，即使 OS lock 已释放，
也不符合本方案的并发和恢复 SLA。

除第 15 节已持有 exclusive barrier 的 GC maintenance 专用提交外，所有 campaign/maintenance event
commit（包括不新增对象的 control/lease event）都先取得同一全局 `cas-reference.lock` shared 屏障。
统一锁序扩展为：

```text
CAS reference barrier
  → 按规范 key bytes 排序的 cache-key/provider-slot resource locks
  → maintenance chain lock（若需要）
  → 按 campaign_id 排序的 campaign chain locks（若需要）
```

单 campaign 普通事件可跳过不相关层级，但任何代码路径不得反向取得。Cache observation/classification、
attach、resolve 和 completion check 使用同一 cache-key lock；全局 provider slot admission 使用对应
provider-slot lock。需要同时触及 maintenance 与 campaign chain 的操作必须使用第 8.2 节定义的显式
pending saga，不能声称两个 event 文件构成一个原子事务。
若 event 将引用新对象，先在 CAS 目录之外准备、校验并 `fsync`
临时对象；再取得 shared 屏障和对应 chain lock，在屏障内原子安装或验证 CAS 对象、核对 parent/
revision/writer fencing token/可选 attempt lease token，按本节 pending-write + no-replace 协议安装下一个
不可变 event 并持久化目录，最后用 SQLite transaction 更新投影。只有 event 成功提交后对象才成为 live
reference。外部 provider 调用不持有任何上述锁。

若 event 已写而 SQLite 更新前崩溃，恢复时重放 event chain；若只安装了内容对象而没有 event，
对象视为 orphan，只能按 GC 规则回收。GC dry-run 只能生成候选 manifest；真实 execute 必须先取得
同一屏障的 exclusive 模式，等待已有共享提交完成，在屏障内重扫全部 event heads/对象引用并按
第 15 节的可恢复 transaction 完成隔离移动。这样扫描与 event commit 之间不存在“新对象刚被引用却被 GC 移走”的窗口。损坏、断号、
parent 不匹配或 fencing token 倒退必须失败关闭，不能猜测补链。

并发上限是跨进程的权威 admission，不是某个 `audit run` 进程内的 worker 数。Policy/authorization
同时冻结 campaign cap、provider/deployment pool cap 和 `bundle_kind × risk_class` cap；实际允许值取
所有适用 cap 与 CLI `--concurrency` 的最小值，CLI 只能进一步降低。每个 cap 都以未 terminal 的
active lease 计数，lease 仅仅 wall-clock 过期而尚未提交 canonical expiry terminal 时仍占 slot。
Campaign reauthorization 可以降低自己的 cap；提高全局 provider/risk pool cap 需要单独版本化的
repository policy authority，不能由任一 campaign authorization 单方面放大。

```text
provider_pool_key = H("provider-concurrency-pool-v1", {
  provider,
  resolved_deployment_id,
  bundle_kind,
  risk_class
})
```

若 policy 还规定 provider-wide cap，另对不含 bundle/risk 的 parent pool 同时 reserve；多 pool locks 按
key bytes 排序取得，attempt 必须在每个适用 pool 都有 slot，不能用更细粒度 pool 绕过全局 cap。
Pool resource identity 不随 policy version 改变；每个 admission event 另保存 policy version/cap snapshot，
更新 policy 时仍在同一 pool 下计入旧 active slots。

跨 campaign 的 provider slot 使用 maintenance chain 中的可恢复三步 admission：

```text
provider-slot-reservation-pending
  → campaign attempt-started
  → provider-slot-activated
  → provider-slot-released（仅在 canonical attempt terminal 后）
```

调度器按统一锁序同时持有 provider-slot resource lock、maintenance lock 和目标 campaign lock：先从
maintenance event chain 计算全局 pending+active slot，从 campaign chain 计算本 campaign active attempts，
再提交带唯一 `slot_reservation_id` 的 pending reservation；随后提交引用它的 `attempt-started`，最后
激活 slot。Pending 从第一步起就占并发额度，provider 只有在三步均 durable、writer release 已提交且
所有锁已释放后才可启动，因此跨链崩溃最多泄漏 slot，不会超发调用。恢复规则唯一：若只有 pending
而不存在匹配 `attempt-started`，释放 pending；若 attempt 已创建但 slot 未 activated，provider 依契约
不可能已经启动，recover 一律以 pre-transfer composite cancellation 关闭 attempt/round 并释放，不根据
进程存活猜测是否补激活；同 ordinal 可按第 9.3 节规划 successor instance。若 attempt
已 terminal 但 slot 未释放，补提 release。任何一步都以 slot/attempt digest 幂等，不能从 SQLite
计数猜测。Campaign 内的 active-count 检查与 `attempt-started` 在同一 campaign lock transaction 内，
因此两个 CLI 即使同时指定 `--concurrency 2` 也无法合计启动第三个 attempt；翻译或高风险 cap=1 时
第二个同样在 admission 前被阻断。

外部调用期间不持有 campaign lock。调度器先提交 `attempt-started` event；其 payload 必须完整
包含 `attempt_lease_token`、owner、issued/expires time、attempt/run/authorization ID、冻结的 review request
instance ID、transport attempt ordinal、parent attempt、stage、work-unit instance、task ID 与 task revision、bundle/result cache
key、provider/model alias/resolved deployment/lineage/mapping digest、thinking、timeout、
`completion_commit_grace_seconds`，以及逐维预算字段：`reserved_calls=1`、input/output token（hard
模式使用 certified upper bound reservation，forecast 模式只保存预测值）、按第 6.3 节
得到的 cost/currency 或明确 disabled、reservation/pricing
policy/version、授权前后预算 snapshot digest。
`attempt-started` 必须与预算准入、reservation 创建在同一个 event commit 中完成；没有成功提交该
event 就不得启动 provider，不能先只在 SQLite 扣减或先发出网络请求。
它还必须引用已预留的 `slot_reservation_id`，保存所有适用 concurrency cap、admission 前后 active
count 和 `concurrency_admission_snapshot_digest`；缺少随后 durable 的 `provider-slot-activated` 也不得
启动 provider。
lease token 是本地并发 nonce，不是 provider credential，但仍按 artifact 最小权限保护。SQLite
attempt/lease 表的每个字段都必须能从 `attempt-started` 及后续 lease event 重建，不能保留
SQLite-only 字段。

Runner 在真正把 payload 交给 provider 的不可逆调用之前，必须提交引用 attempt/reservation/bundle
digest 的 `external-transfer-started` event。该 event 之后 calls reservation 永久转为一次已用调用；
即使进程在 event 与网络调用之间崩溃也按“可能已外发”保守结算。只有 event chain 中不存在
`external-transfer-started` 时，才允许证明 `external_transfer=false` 并使用 pre-transfer cancel。
Provider adapter 在取得可信 request/response ID、远端 acknowledgement 或等价回执时另提交
`provider-request-confirmed`（也可原子内嵌于 attempt terminal）。前者计入
`charged_or_possible_transfers`，后者计入 `provider_request_confirmed`；任何报告都不得把前者描述成
网络请求已被 provider 实际接收。

调用结束后重新进入提交临界区；只有 task revision、attempt 与 event chain 中的 lease token/expiry
仍匹配且未被显式取代时，才能提交 canonical terminal。无 strict validated output 的 terminal 类型为
`attempt-failed`、`attempt-failed-before-transfer`、`attempt-stale`、`attempt-lease-expired`、
`attempt-lease-expired-before-transfer`，或 active pre-transfer 时的
`attempt-and-round-cancelled-before-transfer` composite；它们
原子携带 reservation digest、usage/settlement 字段和可选 provider raw-usage object digest。

存在 strict validated output 时禁止先提交一个孤立的 `attempt-completed`，再另写 round/final acceptance。
规范 terminal 必须是一个 campaign composite domain event：普通 round 使用
`review-round-validated`，独立终审使用 `independent-final-validated`，remediation 使用
`remediation-result-validated`；三者都内嵌唯一
`attempt_terminal={kind: completed, reservation, usage, settlement, raw_usage_digest}`，同时关闭 attempt、
从 campaign active count 移除并令全局 provider slot 可释放、接受唯一 request result，并原子应用完整
ledger/candidate-result delta。实际全局 slot 仍由紧随其后的 maintenance `provider-slot-released`
关闭。第 8.3 节可把其中 terminal 子记录投影为 `attempt-completed` 指标，但不得再创建第二个
事实事件。这样不存在“attempt 已 terminal、request 却没有可恢复 acceptance”的普通路径。

因为 validated observation 的全局分类在 maintenance chain、目标 ledger 在 campaign chain，二者
使用第 8.2 节的 `classified-pending-target → target-committed → flight-closed` 可恢复 saga，而不冒充
跨文件原子事务。分类 event 先引用 validated CAS object 并冻结 cache-key generation；随后在同一
cache-key lock 持有期内提交上述 campaign composite event，最后关闭全局 flight。若在分类后、target
commit 前崩溃，active flight 阻止其他 observation/attach；`audit recover` 只能依据 request、termination
在同一 campaign chain 中相对 target composite 的 sequence 和分类 certificate 补提唯一结果：尚无
termination 时正常 eligible 结果完成 ledger acceptance，
已先请求 termination 的结果则以 `attempt-result-unattached-and-round-abandoned` composite 结算并关闭
round，conflict 则以 `attempt-result-blocked-by-cache-conflict` composite 结算 attempt 并把 request
置为 `awaiting-cache-resolution`。若 target composite 已存在而 flight 尚未关闭，recover 只补
`cache-flight-closed`。任何分支都不会重跑 provider、产生第二 terminal 或选择另一份结果。

若 request 已有 accepted result，其他 completion 即使 schema 合法也只能使用
`attempt-result-ineligible` composite 结算为 audit-only provenance；它不得写第二套 ledger delta，也
不得成为 validated cache observation。显式 force 使用新的 request/flight，不能借该分支混入。
分类/接受前后均须再次验证 request 唯一性、cache generation、termination precedence 和 lease；SQLite
指针不是判据。

每个 attempt 恰有一个 canonical terminal。Transfer possible/unknown 的 `attempt-lease-expired` 是调度/
结果终态并按 reservation 保守结算；明确 no-transfer 的 subtype 按上文释放。任何 expiry terminal
之后到达的 provider 响应不能再提交 `attempt-stale`，只能追加非 terminal 的
`attempt-late-response-recorded`，引用原 terminal/reservation、保存去敏 raw/usage digest，并明确
`result_eligible=false`；若已知 actual debit 大于当前 settled debit，再追加或内嵌单调非负的
`attempt-settlement-adjusted` delta。Late response/adjustment 永不减少 debit、改变 task/review 状态或
进入成功缓存。Hard lease-expiry settlement 已保留 certified maximum，正常 provider actual 不应再
增加 hard debit；若仍超过，按 `budget-integrity-failure` 处理。若 campaign 已 terminal，则在其 chain
追加 state-neutral incident reference，并在 maintenance chain 创建 `post-terminal-integrity-incident`，
阻断该 mapping 的后续外发并令导出报告显著标记授权完整性受损，但不篡改历史 review disposition。
对同一 provider response ID 重放必须幂等；无法唯一去重时保守记录证据但不重复计费。

即使执行期间删除并重建 SQLite，持有正确 token 的 completion 仍应通过；错误、过期或已替换 token
一律成为 stale。`audit recover`
取得新的 writer fencing token 后，才可对过期 writer/attempt lease 提交 `writer-lease-expired` 或
按 transfer proof 选择 `attempt-lease-expired[-before-transfer]`；不能只在 SQLite 中静默改状态，也不能
修改或删除旧 event。晚到响应按上段
非 terminal 协议保留证据，但不能覆盖新 revision、当前状态或成功缓存；预算按第 6.3 节的保守规则
结算，不能因 lease 过期自动返还。maintenance event chain
使用相同的 writer lease/fencing 契约和独立的 maintenance lock。

Round 终止使用一个穷举 reducer，而不是分别描述 cancel、expiry 和 abandon。业务 precedence 只比较
同一 campaign chain 中的 target composite 与 `termination-requested`：前者先 commit 才算
validated-before-termination；仅完成本地 validator 或 maintenance classification 不算业务 acceptance。
`termination-requested` 一经提交就禁止新 plan/request/attempt/retry/repair；已经 commit 的 validated
round/final 事实保留，但尚未 commit target composite 的模型响应不能越过该 sequence 变成业务 acceptance。
若 task 关联 active cache/provider resource，terminate 命令也必须按统一顺序取得这些 resource locks，
并在 event 中冻结 observed flight/classification/slot digests，避免跨 chain 用不可比较的 sequence 猜先后。

| termination 时的 request/attempt 状态 | transfer 事实 | 唯一归约 |
|---|---|---|
| round/request 已规划，从未创建 attempt | 无 | `review-round-cancelled-before-transfer` |
| attempt active | 该 request 的所有 attempt 均无 `external-transfer-started` | 单一 `attempt-and-round-cancelled-before-transfer` composite：terminalize attempt、释放 reservation/slot、关闭 round |
| attempt 已 failed/expired，request 尚可 retry | 所有 attempt 均无 transfer | 禁止 retry；`review-round-cancelled-before-transfer` 引用该 request 的完整 terminal-attempt set；已经由 pre-transfer terminal 释放的 reservation 不重复调整 |
| attempt active | 已有 transfer | 等待 provider completion 或由 recover 提交 lease expiry；随后用同一 terminal composite 或紧邻的确定性 `review-round-abandoned-after-transfer` 保守结算并关闭 round |
| attempt 已 failed/expired | 已有 transfer | 禁止 retry；recover/drive 补提 `review-round-abandoned-after-transfer`，保留 calls/token/cost |
| validated result 已全局分类但 target composite 未 commit | 任意 | target 尚未业务接受；若 termination 先 commit，提交 `attempt-result-unattached-and-round-abandoned`；若 recover 先 commit target composite，则后续 termination 保留 acceptance |
| `review-round-validated`/`independent-final-validated` 已 commit | 任意 | 不反转 ledger；该 round 已 terminal，只结算剩余 slot/saga 后进入外层目标 terminal |
| `awaiting-cache-resolution` | 已结算 attempt | 终止时关闭为 `review-round-abandoned-after-conflict`；保留 observation/conflict，不等待人工 resolve |

Remediation request 使用同一乘积表：无 transfer 时取消 request/attempt，有 transfer 时 terminal 后进入
`remediation-abandoned-after-transfer`，已 commit 的 `remediation-result-validated` 保留 candidate/advice
审计事实但终止请求禁止后续 accept/apply。其 cache classification、slot 和 reservation 也必须 drain；
不能因为它不写 finding disposition 就遗漏 active work。

“所有 attempt 均无 transfer”可由不可变 chain 证明，因为 provider launch 的硬前置是 durable
`external-transfer-started`；此时 `attempt-failed-before-transfer`、
`attempt-lease-expired-before-transfer` 和 cancellation 均可释放自己的 reservation。无法证明是否 transfer
则按 post-transfer 分支保守扣减。一个 request 曾有任一 transfer 后，整个 round 不能再使用
pre-transfer 名称，即使最后一个 retry 尚未 transfer。

Active pre-transfer attempt 与 round 必须由一个 composite event 同时关闭，不再制造“attempt 已
lease-expired/cancelled、round 却等另一个不可达 terminal”的窗口。对于历史上已经 terminal 的
pre-transfer attempts，round cancel event 必须引用完整 attempt set、证明不存在 active reservation/
slot，并且不重写它们的 terminal。Post-transfer attempt terminal 与 abandon 若因 provider adapter
路径不能编码为一个 composite，前一个 event 必须显式产生 `abandon-pending`；在该状态下禁止任何
业务 transition，`audit recover` 被明确授权补提唯一 abandon event。

`audit recover`/`drive` 可在不调用 provider 的情况下执行上表所有唯一转换，包括 pre-transfer
cancel、post-transfer abandon、cache-flight 收尾和 outer drain terminal；它们不能选择 finding
disposition或发起 retry。External transfer 后的 abandon 是 round 失败终态，晚到结果只作 stale/audit
observation，不能释放已用预算、重写 frozen bundle或借下一 continuity ordinal 重发同一语义输入。

### 8.2 审计 envelope 与语义缓存键

本地审计身份和模型实际看到的语义输入必须分层。模型可见的
`model_semantic_payload` 只包含完成判断所需的当前公开内容、依赖、规范 prior finding/reply/evidence
和合同指令；不得包含 campaign/task/round instance/authorization ID、event/CAS 路径、预算、时间戳、
本地 `R-NNN` 或其他仅用于调度和审计的字段。Item/path/finding 使用按规范内容顺序分配的短 alias；
alias 到本地 ID/ref 的完整映射只存在于本地 envelope。`payload_digest` 是精确 outbound canonical
bytes 的哈希，而不是含本地元数据的 JSON 哈希。

```text
payload_digest = H("outbound-semantic-payload-v2", exact_outbound_canonical_bytes)

semantic_round_context_digest = H("semantic-round-context-v2", {
  prior_validated_semantic_findings,
  codex_reply_semantic_projection,
  current_revision_and_dependency_digests,
  semantic_contract_flags
})

result_cache_key = H("validated-review-result-cache-v2", {
  payload_digest,
  semantic_round_context_digest,
  prompt_digest,
  contract_version,
  redaction_version,
  provider,
  resolved_deployment_id,
  model_lineage_id,
  thinking,
  validator_version,
  decode_config_digest
})

bundle_digest = H("local-review-audit-envelope-v3", {
  result_cache_key,
  campaign_id,
  work_unit_instance_id,
  task_id,
  plan_revision_id,
  review_request_instance_id_or_null,
  authorization_id_or_null,
  local_alias_mapping_digest,
  local_policy_and_termination_digest
})

transport_config_key = H("provider-transport-config-v1", {
  result_cache_key,
  timeout_seconds,
  transport_config_digest
})

attempt_id = H("provider-attempt-instance-v3", {
  campaign_id_or_null,
  run_id,
  review_request_instance_id,
  attempt_start_event_sequence,
  transport_attempt_ordinal,
  external_authority_digest,
  transport_config_key
})
```

`prompt_digest` 只覆盖真实发送给模型的指令；campaign 名称、授权摘要或本地报告模板不能混入。
`semantic_contract_flags` 至少包含 review role（initial/continuity/independent-final）、要求的输出合同和
会影响判断的 policy flags，但不包含 ordinal、remaining budget 或本地 terminal metadata。
`resolved_deployment_id` 是 provider-qualified immutable serving identity；`model_lineage_id` 是可
跨 alias/provider 识别的 underlying weights/release lineage。两者均来自第 6.3、13.4 节冻结 mapping，
不能使用易变 alias 替代。`decode_config_digest` 覆盖 max output、response schema、temperature/seed
等影响模型输出的生成设置；timeout 和网络传输只进入 `transport_config_key`。`attempt_id` 再绑定
campaign/run、冻结 request、event-chain 中唯一的 start sequence、transport ordinal 和外发 authority，
因此两个 campaign、两次 `--force` 或两个 worker 不会因相同 result key/ordinal 撞成同一执行。
Campaign 模式的 authority digest 是 authorization ID；Phase 0 的 `campaign_id=null` 时使用本次用户
确认 digest，`review_request_instance_id` 由 run/bundle/result key/request generation 构造，并由
maintenance chain sequence 与 `run_id` 提供同等唯一性。所有对象继续使用
第 6.1 节带 domain 和 type/length framing 的 `H`，禁止裸字段拼接。

语义 finding slice 包含当前 finding key、family/continuation 的内容关系、各 evidence 的
item/revision/anchor、severity/category、resolution condition、lifecycle status 和上一轮 Pi status，
再按规范内容生成 `f01`、`f02` 等 alias。它明确排除本地 `finding_ref`、标题改写、event ID、作者/
approver、wall-clock、usage、budget、lease 和 CAS 路径；Codex reply 只投影模型判断所需的 stance、
revision 与公开 evidence，不复制本地审计元数据。Family/continuation 以规范 alias edge 表达，不携带
campaign-local family/ref ID。`local_alias_mapping_digest` 则把本轮短 alias 精确
绑定到本 campaign 的 item ID 和 `finding_ref`，用于回收输出，但不外发、不进入结果缓存键。

同一语义输入在不同 campaign、周期性触发或本地 `R-NNN` 编号下应得到同一 `result_cache_key`，即使
各自的 `bundle_digest` 不同。缓存对象保存模型 alias payload、validator proof 和 resolved
deployment/model lineage，不保存可被下一 campaign 误用的本地 ref 映射。命中时 adapter 必须使用当前 bundle 的 alias
映射重新验证/物化新的本地 validated envelope，并提交上述
`review-round-validated(source=cache)` composite event；不能直接复制来源 campaign 的 disposition events。

全局 cache 状态由 maintenance chain 中按 `result_cache_key` 单调递增的
`cache_classification_generation` 归约，SQLite observation 表不是事实来源。所有 miss admission、
`--force`、validated observation 分类、cache attach、`cache-resolve` 和 campaign completion recheck
必须取得同一个 cache-key OS lock；没有该锁时不得读取后写入“当前 observation set”。每代 certificate
至少包含完整规范 observation-set digest、equivalence classes、chosen representative 或 conflicted、
上一代 digest、active flight 和 reducer/version。

为避免并发冷 miss 重复付费，每个 key 最多有一个 active observation flight：

```text
cache-flight-started(kind=normal-miss|force|fresh-final|remediation, generation=n)
  → provider attempt(s), no cache-key lock held while waiting
  → cache-observation-classified-pending-target(generation=n+1)
  → target campaign composite committed | target-ineligible/conflicted committed
  → cache-flight-closed
```

`cache-flight-started` 在 maintenance chain 中 durable 后才允许创建对应 campaign attempt；普通 miss
遇到 active flight 时加入本地 wait/recheck 队列，不创建 reservation 或第二次外发。Force 也串行等待，
但保留自己的 reason/authority/observation generation，不能绕过已有 flight。Flight lease 过期只允许
recover 根据 campaign attempt/transfer/terminal 事实继续或关闭，不能让第二个 flight 与未知旧请求并发。
普通 review/remediation miss 的等待者可在前一 flight 产出 eligible observation 后 attach；`--force` 和
`fresh-final` 的等待者只被串行化，前一结果不能履行其“新增 observation/本 instance fresh execution”
义务，前一 flight 关闭后仍须以新的 generation 启动自己的 flight。
若 flight 建立后 attempt budget/concurrency admission 失败且尚无 `attempt-started`，必须提交
`cache-flight-cancelled-before-attempt` 立即释放；不能让本地 admission failure 占用 key。
Flight 的 pre-attempt admission TTL 是短 policy 值；一旦绑定 `attempt-started`，expiry 必须至少覆盖该
attempt lease、所有已授权串行 retry/repair transition 和 completion grace，或由每次 successor event
显式续期。Wall-clock expiry 本身不释放 flight，只有 recover 的 chain-derived terminal 才释放。

Validated output 到达时，runner 按统一锁序持有 cache-key、maintenance 和 target campaign locks：
先用 conservative reducer 提交 `cache-observation-classified-pending-target`；若新 observation 与既有 class
非等价，该 event 本身就把 generation 标为 conflicted，当前 target 不获得普通 validated acceptance。
随后提交第 8.1 节的 campaign composite terminal/acceptance或 conflict/ineligible outcome，最后关闭
flight。三个 event 各自 crash-atomic，但不是跨链原子；显式 pending state 和唯一 digest 令每个崩溃点
可由 recover 幂等完成。分类 pending 时禁止其他 flight、attach、resolve 或 campaign successful
completion。

普通 cache attach 也必须在 cache-key lock 内读取 current certificate、用 target alias/validator 重验，
并在同一次锁持有期提交引用 exact `classification_generation` 与 `observation_set_digest` 的 target
`review-round-validated(source=cache)` composite。`audit verify` 在 successful completion 前按 key bytes
排序取得该 campaign 所依赖的全部 cache-key locks，确认每个 acceptance token 仍指向 current、
unconflicted generation且不存在 pending target；检查与 `campaign-completed-verified` 提交期间不释放这些
key locks。之后才开始的新 observation 可以形成新的 incident/conflict，但不能与该 completion 冒充
同时成立。`cache-resolve`、新增 observation 和 attach 使用同一 generation CAS 规则；stale generation
一律重读或拒绝。

只有通过对应 validator version 的结果可以进入缓存 observation set。失败、超时、空输出、stale
completion 和未经验证的 raw output 不得作为 validated observation。每个 observation 保存
`validated_result_digest`、版本化的 `decision_projection_digest`、来源 attempt 和完整 validator proof：

- canonical validated result 完全相同则是 exact duplicate；
- 只有 versioned conservative equivalence reducer 证明 finding identity/severity/status/context request/
  第 13.2 节 campaign-neutral `semantic_candidate_effect_digest`/eligibility 等所有权威判断相同，才可归入同一 decision equivalence class；无法证明时按
  非等价处理，不能靠标题或自由文本相似度合并；
- 一个未冲突 equivalence class 有多个 observation 时，以规范最小 `validated_result_digest` 作为 attach
  representative，其余仅作 provenance；不能用完成时间或目录顺序挑“最新”；
- 同一 `result_cache_key` 一旦出现两个非等价 validated class，分类 composite 原子生成
  `cache-conflict-detected` 子事实，key 进入 `conflicted`。当前 observation 的 target commit 只能进入
  `awaiting-cache-resolution`，所有未来自动 attach、`task-verified-from-cache` 和 force 结果的自动
  verified 均被阻断；active campaign 在持有同一 key lock 时记录引用该 classification certificate 的
  conflict state。历史已经完成的 campaign 保持不可变，只允许追加 state-neutral incident reference
  并在报告中显著引用冲突；
- 冲突只能通过符合独立性条件的新审核，或 `audit cache-resolve` 的显式用户 authority 选择/弃用某个
  class 来处置。Resolution 必须在 cache-key lock 下绑定当时完整 observation set 与前代 generation；以后新增非等价 observation 会重新打开
  冲突。Resolution commit 后，处于 `awaiting-cache-resolution` 的 target 只能以
  `review-round-validated(source=cache-resolution)`/对应 remediation variant attach 被选 representative；
  原 attempt 已 terminal，attach 不再结算 usage。保守默认是创建 fresh independent review，而不是任意
  挑选“最新”结果。

`--force` 只绕过本次精确缓存读取，必须提供 `--reason`，写入 `cache-bypass` event 并创建新的
observation request/attempt；不得覆盖、删除或悄悄切换原 validated result，也不得超过授权的
`max_forced_observations`。
若 target round 尚未形成 validated ledger，force result 可作为该 round 的唯一
`review-round-validated` 来源；若 round 已有 validated ledger，等价 observation 只增加 provenance，
非等价 observation 触发 conflict，两者都不能提交第二份 ledger delta。

执行顺序固定为：构建当前 local audit bundle，验证 plan-scoped generation/count、公开 allowlist、
scope、本地 cache-use policy 和 resolved deployment/model lineage，再计算语义 key；取得 cache-key lock，
查询 current classification certificate 并以当前 alias 映射与 validator 复验精确 cache。未冲突的 cache
hit 在该 lock 下直接 attach；不要求 external-transfer authorization，也允许在 `calls_remaining=0` 或
尚无 authorization 时命中。若 key 已有 active flight，先等待/recheck，不要求等待者取得外发授权。
只有既无 hit 也无 active flight 的 cache miss 才停在 `awaiting-external-authorization`，此时不占全局 flight，
避免等待人工确认期间阻塞其他 campaign。取得 authorization 后、真正 attempt admission 前，再在
cache-key lock 下做一次 just-in-time recheck；若仍 miss/force/fresh-only，才取得唯一
`cache-flight-started`，然后进入 attempt-scoped concurrency/预算准入、reservation 和
`attempt-started`。等待既有 flight 不消耗调用；等待期间若 observation 到达则直接 recheck/attach。
Cache hit 的 `external_transfer=false`、
usage 为 0，不创建 attempt/lease/reservation；但不能绕过当前 campaign 的 scope、generation、bundle
kind、revision、local policy、cache conflict 或 completion gate。

### 8.3 Usage 与成本事件

每次 cache decision 都进入 event chain：miss/bypass 使用独立 decision event，hit 进入上文
`review-round-validated.cache_attachment` 复合事实。每个 provider attempt 的 canonical terminal 或
validated-result composite 都携带同一个 `attempt_terminal` usage/settlement 子记录，不再另写第二条
completion 事实。下面展示的是可由 event 重建的统一 projection；`source_event_type` 指明它来自普通
terminal 还是 round/final composite。字段缺失时使用 `null`，不能伪造为零：

```json
{
  "schema_version": 3,
  "record_kind": "attempt-terminal-projection",
  "source_event_type": "review-round-validated",
  "terminal_kind": "completed",
  "campaign_id": "...",
  "run_id": "...",
  "authorization_id": "...",
  "stage": "initial-review",
  "work_unit_instance_id": "...",
  "task_id": "...",
  "review_request_instance_id": "...",
  "attempt_id": "...",
  "transport_config_key": "...",
  "result_cache_key": "...",
  "bundle_kind": "code",
  "provider": "opencode-go",
  "model_alias": "...",
  "resolved_deployment_id": "...",
  "model_lineage_id": "...",
  "model_alias_mapping_digest": "sha256:...",
  "thinking": "...",
  "estimated_prompt_tokens": 1400,
  "estimated_completion_tokens": 400,
  "input_token_budget_mode": "hard",
  "output_token_budget_mode": "hard",
  "certified_input_token_upper_bound": 1400,
  "certified_output_token_upper_bound": 400,
  "hard_bound_method": "provider-tokenizer-and-enforced-output-cap-v1",
  "hard_bound_proof_digest": "sha256:...",
  "prompt_tokens": 1200,
  "completion_tokens": 340,
  "token_source": "provider",
  "token_estimator_version": "token-estimator-v1",
  "calibration_bucket": "opencode-go/deployment-lineage/code/initial-review/v1",
  "calibration_fallback_level": 0,
  "prompt_actual_estimate_ratio": 0.8571,
  "completion_actual_estimate_ratio": 0.85,
  "elapsed_ms": 8421,
  "timeout_seconds": 1200,
  "cache_status": "miss",
  "transport_attempt_ordinal": 0,
  "payload_repair_generation": 0,
  "exit_reason": "validated",
  "bytes_in": 8192,
  "bytes_out": 2048,
  "external_transfer": true,
  "transfer_state": "provider-confirmed",
  "provider_request_confirmed": true,
  "provider_request_id_digest": "sha256:...",
  "budget_reservation_digest": "sha256:...",
  "reserved_calls": 1,
  "reserved_input_tokens": 1400,
  "reserved_output_tokens": 400,
  "settled_calls": 1,
  "settled_input_tokens": 1200,
  "settled_output_tokens": 340,
  "provider_raw_usage_digest": "sha256:...",
  "cost_budget_mode": "disabled",
  "reserved_cost_amount": null,
  "settled_cost_amount": null,
  "cost_amount": null,
  "cost_currency": null,
  "cost_source": "unavailable",
  "pricing_version": null,
  "pricing_snapshot_digest": null,
  "recorded_at": "2026-08-01T00:00:00Z"
}
```

`external_transfer=true` 是兼容字段，只表示存在 `external-transfer-started`，即“已计费或可能外发”，
不是 provider receipt。权威字段 `transfer_state` 只允许 `not-started`、`possible`、
`provider-confirmed`；最后一态必须有可信的去敏 request/response digest。完成报告至少分别输出：

- `attempts_reserved`：存在 `attempt-started`；
- `charged_or_possible_transfers`：存在 `external-transfer-started`；
- `provider_request_confirmed`：存在可信 provider acknowledgement；
- `validated_results`：通过 strict validator 并原子进入 review/cache observation。

`token_source` 只能为 `provider`、`estimated` 或 `unavailable`。cache hit 也产生事件，但
使用 `review-round-validated.cache_attachment` 的非-attempt usage variant：`attempt_id=null`、
`external_transfer=false`、`transfer_state=not-started`、token 为 0、`exit_reason=cache-hit`，且没有 lease/reservation/terminal；
不能伪造一条 `attempt-completed`。只有
cache miss/`--force` 才做外部调用准入：hard token 维度按 certified upper bound reservation，结束后
按 provider actual 结算但绝不超过已证明上界；forecast token 维度仅记录估算/actual，不作为授权
扣减或阻断依据；disabled 可为 `null`。没有 provider usage 时，hard 保留 reservation，forecast
保留 estimate 与来源。
`cost_source` 同样明确区分 provider、版本化 price table 和 unavailable。usage event 不包含
凭据、原始 prompt、受保护路径或模型 raw output。

当 `cost_budget_mode=disabled` 时，cost reservation/settlement/pricing 可以为 `null`；当
`cost_budget_mode=forecast` 时只记录预计/实际值，不得称为授权 ceiling；当 `cost_budget_mode=hard` 时，
`reserved_cost_amount`、currency、pricing version/snapshot digest 和最坏情况证明必须在
`attempt-started` 中非空且进入 reservation digest，terminal event 必须给出数值
`settled_cost_amount`（provider actual 不可用时等于 reservation）。模式或 pricing snapshot 的变化
必须通过新的完整 authorization revision；它影响本地 admission，但语义输入不变时不污染
`result_cache_key`。

只有 `token_source=provider` 且 estimate 非零时才计算 actual/estimate；cache hit、provider 未
返回 usage 或估算不可用时 ratio 为 `null`，不能用估算值冒充 actual 样本。

token estimator 按 `(provider, resolved_deployment_id, model_lineage_id, bundle_kind, stage,
estimator_version)` 分桶记录
actual/estimate 比率；`stage` 至少区分 `initial-review`、`review-reply`、`evidence-supplement`、
`remediation`、`payload-repair` 和 `final-review`，避免把含历史上下文的后续 round 与初审混为同一
分布。每桶的历史 p90 只用于 bundle packing、吞吐预测和 `forecast` 维度；样本不足时依次回退到
同 deployment/lineage 但去掉 stage、同 provider/lineage 的兼容 deployment、再到 provider/kind 的
上级桶，仍不足时使用固定预测系数，并记录 calibration bucket/fallback level。P90、固定
“安全系数”或历史经验都不能充当 hard reservation 的上界证明。Hard admission 只使用第 6.3 节的
certified bound；其 remaining 不足时提交 `budget-admission-blocked`，明确 required、remaining、证明
方法、预算维度和建议动作。不能用本轮尚未知的 actual 反向改变已生成的 payload/bundle ID。

calibration snapshot digest 与 estimator version 必须进入本地 `policy_digest`，并在 authorization
revision 内冻结。Forecast actual 超过预测只产生 `forecast-variance-recorded`，不会被误报为授权越界；
hard actual 超过 certified bound 则提交 `budget-integrity-failure`、禁止新 attempt，并在 drain 后
终止 campaign，因为这表示
tokenizer/provider contract 失效，而不是允许事后补记的普通 overrun。

Phase 0 尚未建立 campaign 时，`campaign_id=null`、`run_id` 必填，usage/cache/timeout 事件写入
maintenance event chain。进入 campaign 后两者均保留：`campaign_id` 表示累计授权和完成范围，
`run_id` 表示一次 CLI/resume 执行，便于同时统计 per-run 与 per-campaign 预算。

## 9. 受控证据请求

### 9.1 Evidence request

Reviewer 可以返回可选的 `context_requests`：

```json
{
  "context_requests": [
    {
      "item_alias": "i03",
      "kind": "related-public-diff",
      "reason": "需要确认调用方是否依赖该返回结构"
    }
  ]
}
```

允许的 request kind 使用固定白名单，例如：

- `related-public-diff`
- `public-symbol-signature`
- `existing-test-expectation`
- `translation-neighbor`
- `terminology-context`
- `similar-public-pattern-occurrences`

宿主必须校验 request kind、目标 work-unit/task、公开路径、条目数和字节数仍位于 campaign 本地 logical scope/
policy 内，只提取最小公开证据，并重新执行绝对路径与受保护信息检查。若证据 cache miss 后需要
外发，current external authorization 还必须明确覆盖 `evidence-supplement` stage、该 logical scope 和
预算；cache hit 本身不要求外发授权。请求引入新的 task/path/content kind 时
属于 scope drift，不能以“补充证据”为名复用授权。任意路径、仓库遍历、源码工具、凭据、
网络或受保护输入请求一律拒绝。

`similar-public-pattern-occurrences` 不能携带任意正则或路径 glob。它必须绑定当前 finding 的
`rule_id`、item alias 和规范 evidence anchor，由宿主使用受审计的本地匹配器，仅在当前公开
allowlist 内返回固定上限的 path/item alias、anchor 和最小上下文；默认最多 20 个 match、5 个文件。
超过上限只返回截断计数并要求重新 plan，不能自动遍历或外发整个仓库。命中新的 task/path 时仍按
scope drift 处理，不因“类似模式”获得隐式授权。

补充证据形成新的 bundle revision，但仍属于同一 campaign work-unit lineage。默认只允许一次补充，
split/merge 后也不能复制该 entitlement。

证据不能只靠文中提到的 event 自动出现。低层状态机固定为：

```text
context-request-validated
  → evidence-supplement-validated
  → evidence-supplement-accepted (new plan generation embedded)
  → codex-response-recorded
  → review-round-prepared
```

`audit evidence-attach` 只用 SafePublicFileResolver 提取/接收白名单 kind 的最小公开 artifact，并校验
request binding、path/item、bytes/match/file cap、taint、redaction 和 current revision，成功最多推进到
`evidence-supplement-validated`。`audit evidence-accept` 要求当前 request、authority 和 validated digest，
并提交一个复合 `evidence-supplement-accepted` event；其 payload 同时固化新的 plan generation、
current task revisions 与 plan revision，不能先接受 evidence 再另行更新 generation。重复同 digest
幂等，第二个非等价 evidence 必须显式 supersede 且仍受
“默认一次”上限。拒绝、越界或过期 request 使用 terminal `evidence-supplement-rejected`，不能留下
既非可重试也非已接受的悬空 artifact。

推荐的高层 `audit prepare-round` 可以把 evidence validate/accept、新 plan revision、当前 reply 校验
和 round freeze 合并为一次本地事务；其 canonical `review-round-prepared` event 必须内含上述各子
结果/digest，其中 evidence 子记录采用与 standalone `evidence-supplement-accepted` 相同的
`evidence_acceptance_id` 和 schema。对同一 acceptance ID，event chain 只能出现 standalone 或 embedded
形式之一；reducer 将二者归为同一种 accepted-chain 事实。它不调用 provider，任何子 gate 失败都不
提交部分状态。

### 9.2 Codex reply artifact

Codex 对审核意见的修复、反驳或补证必须形成 `codex-review-reply-v2` artifact，不能只写入自由文本
日志。它绑定上一轮 validated review 和当前 work-unit/plan/task revision；旧 revision 上的答复不能移植到
新 revision 后继续使用。

```json
{
  "schema_version": 2,
  "contract": "codex-review-reply-v2",
  "campaign_id": "audit-20260801-001",
  "work_unit_instance_id": "sha256:work-unit-g2-task-001",
  "task_id": "task-001",
  "target_continuity_round_ordinal": 2,
  "responds_to_review_digest": "sha256:review-round-1",
  "current_plan_revision_id": "sha256:plan-2",
  "current_task_revision_id": "sha256:task-2",
  "reply_generation": 1,
  "supersedes_reply_digest": null,
  "responses": [
    {
      "finding_ref": "R-001",
      "stance": "fixed",
      "summary": "增加空值分支并补充回归测试。",
      "changed_item_aliases": ["i03"],
      "evidence": [
        {
          "item_alias": "i03",
          "anchor": "hunk:h07",
          "claim": "解引用前已检查输入。"
        }
      ],
      "local_validation_refs": ["test:foo-null-input"]
    },
    {
      "finding_ref": "R-002",
      "stance": "disputed",
      "summary": "该入口只能由完成校验的调用方进入。",
      "changed_item_aliases": [],
      "evidence": [
        {
          "item_alias": "i05",
          "anchor": "hunk:h09",
          "claim": "调用方在进入函数前执行约束检查。"
        }
      ],
      "local_validation_refs": []
    }
  ]
}
```

`stance` 只允许 `fixed`、`partially_fixed`、`disputed`、`needs_context` 和
`accepted_not_fixed`。每个当前 open finding 必须恰好出现一次；未知、重复或上一轮已关闭的
`finding_ref` 一律拒绝。证据只能引用当前有界 bundle 中的 item/anchor 或已验证的本地检查摘要，
不能引用任意路径、自由形式命令输出、Pi session 内容或受保护输入。

`audit respond` 必须把 stance 与实际内容 revision 做本地一致性检查，避免把自相矛盾的 reply 外发：

- `fixed` 必须提供非空 `changed_item_aliases`，其中至少一个 alias 与该 finding 的 evidence、accepted
  candidate 或明确因果关系绑定，并且其 current item revision 与上一轮 reviewed item revision 不同；
- `partially_fixed` 还必须提供非空 `remaining_issue`，说明已处理和仍未处理的边界；其
  `changed_item_aliases` 使用同一变化判据；
- 仅 task dependency、补充 evidence、测试摘要或 policy 变化，不足以证明 `fixed`；不能只比较
  `current_task_revision_id != prior_task_revision_id`；
- `disputed`、`needs_context`、`accepted_not_fixed` 可以保持内容 revision 不变，但必须满足各自的
  evidence/reason 合同。

上述矛盾基线采用失败关闭而不是 warning，因为 warning 后继续外发会浪费有限 continuity round。

Codex reply 表达主代理的立场，不拥有 finding 关闭权。`fixed` 只推进到
`codex-response-recorded`/`re-review-required`；只有后续 Pi disposition、本地验证和必要的独立
复审都满足时，ledger 才能关闭 finding。合同通过后，宿主先把 reply 写入 CAS，再提交
`codex-response-recorded` event；不能只更新 SQLite 或可变 ledger。

对 candidate/host fix，reply 的 current revision 必须是 `record-applied` 或
`bounded-host-revision-accepted`/`exact-host-revision-authorized-and-accepted` 后的 revision；在修改前
预写“将会 fixed”的 reply 无效。对 evidence，reply
可以和 evidence 一起交给 `audit prepare-round`，但 validator 必须先在同一复合 event 的内部顺序中
接受 evidence/new plan revision，再校验 reply anchor。这样不会出现 reply 指向旧 generation，或
candidate 已应用却因缺少 current-revision reply 无法进入复审的断链。

同一 `(campaign_id, work_unit_instance_id, target_continuity_round_ordinal, responds_to_review_digest,
current_task_revision_id)` 的 reply 在 round instance 分配前采用 replace 语义，不做 append 或
stance 合并：新 artifact 的 `reply_generation` 必须严格加 1，`supersedes_reply_digest` 必须指向
当前 active reply；旧对象保留在 CAS，并提交 `codex-response-superseded` event 后才切换 active
指针。乱序 generation、错误 digest 或并发双重 replace 均拒绝。

`review-round-planned` 是冻结点；该 event 提交后，尤其 `attempt-started` 之后，不得替换本 instance
reply 或让同一 instance ID 指向新 bundle。后续修正必须进入 successor instance；若尚未外发但确需撤销，只能
按第 8.1 节取消状态机终止旧 round：没有 attempt 时直接提交
`review-round-cancelled-before-transfer`；有 active reservation 且从未 transfer 时提交单一
`attempt-and-round-cancelled-before-transfer` composite；已有 terminal pre-transfer attempts 时 round
cancel 引用完整 set。已有 `external-transfer-started` 时只能 abandon 且保留 debit。任何路径都不能
重写旧 event 或复用旧 instance ID。

### 9.3 Review round bundle

逻辑 continuity ordinal 与不可变 round instance 分离：

```text
round_instance_id = H("review-round-instance-v2", {
  campaign_id,
  work_unit_instance_id,
  task_id,
  continuity_round_ordinal,
  instance_generation,
  basis_review_digest_or_null,
  frozen_reply_digest_or_null,
  semantic_round_input_digest
})

review_request_instance_id = H("review-request-instance-v2", {
  round_instance_id,
  observation_generation,
  payload_repair_generation,
  prompt_digest,
  contract_version,
  decode_config_digest
})
```

`semantic_round_input_digest` 在分配 instance 前由 current revision/dependency、basis review 的语义投影、
被本次 planning transaction 选中的 validated Codex reply 语义投影和已接受补证确定；它不包含
instance ID、本地 envelope 或最终
`bundle_digest`，从而不存在循环哈希。Instance ID 确定后才能生成本地 bundle digest。

Pre-transfer cancelled round instance 不消耗 continuity ordinal；successor 使用相同 ordinal、递增
`instance_generation`、新的 instance ID，并同时引用 cancelled predecessor 与“最近一次 validated
review”（初审为 null）。每个 ordinal 默认最多 2 次本地 replan instance，超限则 task escalated，
防止无限 artifact churn。Round index 路径必须包含 ordinal 与 instance generation，不能只用整数
round 覆盖旧实例。

一个冻结的 round instance 先产生 `observation_generation=0, payload_repair_generation=0` 的
`review_request_instance_id`。带原因的 `--force` 在 prior request 已 terminal 后递增
`observation_generation`，但不改变 semantic payload/result cache key；它专门用于生成第 8.2 节的
额外 observation，不能复用已关闭 request ID。若模型响应已经外发
但 strict payload 无效，且 authorization 允许一次 repair，则 `payload_repair_generation=1` 使用原语义 bundle、公开
validator error 和新 prompt 生成新的 request instance；repair generation 从当前 observation 分支派生，
不改变 reply/current revision，也不消耗
新的 continuity ordinal。每个 request instance 下允许 `max_transport_attempts` 个严格串行 attempt：

```text
request-planned
  → attempt[0]-started → failed/expired-before-valid-result
  → attempt[1]-started → strict-output-validated-locally
  → cache-classified-pending-target
  → review-round-validated (attempt terminal + request acceptance + ledger)
```

Transport error、provider 5xx、空连接或 timeout 先 terminalize 当前 attempt，再在相同 frozen request
下递增 `transport_attempt_ordinal`；retry 不创建新 round/request，也不改变 result key。任一 attempt
产生 strict-valid payload 后，只有第 8.2、9.4 节 classification + composite target commit 完成，request
才原子进入 `request-validated` 并同时 terminalize attempt；在 `classified-pending-target` 期间禁止再启动
attempt。早期 uncertain
attempt 的晚到响应一律 ineligible。所有 transport attempt 都计 call/token/cost，但 continuity ordinal
只在一个 validated semantic judgment 被 ledger 接受时计一次。若 transport/repair cap 耗尽仍无
validated result，task 进入 `task-failed` 或显式 follow-up，不能创建下一个 continuity ordinal 来规避
失败上限。达到 `max_continuity_rounds` 后不得创建新的 ordinal；按第 9.5 节处置或进入独立终审/新
campaign。

宿主把最新有界内容、上一轮 findings 和 Codex reply 规范化为 `tome4-review-round-v2` 本地审计
bundle；它不附带完整聊天 transcript，并明确拆为两层：

- Local audit envelope：campaign/task、continuity ordinal、round instance/predecessor、request instance/
  payload repair generation、basis review、
  当前 plan/task revision、authorization、resolved deployment/model lineage、预算/终止条件、本地 alias 映射、
  `semantic_round_context_digest`、`result_cache_key` 和最终 `bundle_digest`；
- Model semantic payload：最新公开代码 diff 或规范翻译条目及确定性短 alias/anchor、上一轮未关闭
  findings 的模型短 alias/规范 evidence/resolution condition、经过校验的 Codex reply 语义投影、已
  授权的公开补充证据/本地测试摘要和模型合同；其精确 bytes 产生 `payload_digest`。

Campaign/task/instance/authorization、本地 `finding_ref`、provider 调度信息和预算只留在 envelope，
不进入模型 payload；影响模型判断的任何历史事实都必须进入 semantic payload/context digest，不能
从 Pi session 或进程状态旁路注入。Local bundle 可因 campaign 元数据不同而改变，而语义完全相同的
跨 campaign 输入仍能命中第 8.2 节的 result cache。

Pi prompt 必须明确：以 bundle 内 current revision 为唯一代码/译文事实；逐项判断所有 prior
findings；不要依赖、请求或推断工作区与历史 session；新增问题只能引用当前 bundle 的 item 和
anchor。所谓“重新读取最新代码”在本架构中就是重新阅读本轮 current payload。

同一 work-unit instance 的 round instance 严格串行。初审 instance 固定 `basis_review=null` 且不含 Codex reply；
后续 planning transaction 必须在 chain lock 内选择唯一 basis validated review 和唯一 active
validated Codex reply，计算 instance/bundle，并由同一个 `review-round-planned` event 原子冻结该
instance 的 reply digest。Pre-transfer cancelled successor 默认复用该 exact reply；若确需替换，只能
在旧 instance/attempt 已按状态机完整取消后提交 `codex-response-reopened-after-pretransfer-cancel`，
引用 cancelled instance，再按连续 generation replace，且仍受同 ordinal 最多 2 个 instance 的上限。
External transfer 后禁止 reopen。两个进程不得并发创建同一
`(campaign_id, work_unit_instance_id, continuity_ordinal, instance_generation)`。
晚到、重复、base digest
不一致或引用旧 revision 的结果保留为 stale evidence，但不得进入 ledger 或成功缓存。有效 bundle
写入 CAS 后提交 `review-round-planned` event，request generation 0 同时被冻结；payload repair 只能
通过显式 successor request event，外部 transport attempt 继续使用第 8.1 节 lease/fencing 契约。

### 9.4 Pi disposition contract

Pi 复核只返回受约束 payload，本地 adapter 注入 envelope：

```json
{
  "dispositions": [
    {
      "finding_alias": "f01",
      "status": "resolved",
      "reason": "当前 revision 已覆盖原空值路径。",
      "evidence": [
        {
          "item_alias": "i03",
          "anchor": "hunk:h07",
          "claim": "检查发生在首次解引用之前。"
        }
      ]
    },
    {
      "finding_alias": "f02",
      "status": "still_open",
      "reason": "bundle 中仍存在未经该校验的调用入口。",
      "evidence": [
        {
          "item_alias": "i08",
          "anchor": "hunk:h12",
          "claim": "该调用路径绕过已声明的校验入口。"
        }
      ]
    }
  ],
  "new_findings": [],
  "context_requests": []
}
```

`status` 只允许 `resolved`、`still_open`、`disputed` 和 `insufficient_evidence`；新问题必须放入
`new_findings`，不能伪装成旧 finding 的 continuation。模型可见 payload 不包含 `verdict`；它是
宿主的确定性派生字段，不应要求模型复述。

`actionable new finding` 定义为通过 strict finding gate 且 severity 为 blocker、major 或 minor 的
new finding；note 默认非 actionable，但仍进入 ledger 并需要显式 disposition。模型不能用自报
`actionable=false` 降低严重度。`context_request` 必须绑定某个 `insufficient_evidence` disposition
或同一响应中的 new finding alias；孤立 request 直接拒绝。

Verdict 不是模型自由总结，而是宿主根据 validated payload 重新计算的确定性 reducer，优先级固定为：

```text
if any disposition in {disputed, insufficient_evidence}:
    verdict = disputed
else if any disposition == still_open or any actionable new finding or any context_request:
    verdict = changes_required
else:
    verdict = approved
```

因此同一响应同时含 `still_open` 和 `disputed` 时必须为 `disputed`；非 actionable note 不单独阻止
`approved`，但它一旦绑定 context request 就必须为 `changes_required`；campaign completion 仍要求
该 note 在 ledger 中得到处置。Adapter 验证 dispositions/new findings/context requests 后计算 verdict，
注入本地 validated envelope。兼容旧 provider 合同时，若模型额外返回顶层 `verdict`，adapter 必须在
解析边界确定性丢弃并记录 `ignored-derived-field`，不得因它与 reducer 不同而付费 repair 或拒绝其余
合法内容；除该明确兼容字段外，未知字段仍按当前 strict schema 失败关闭。

本地 validator 必须确认：

- 每个传入的 open finding alias 恰好有一个 disposition，且没有未知或重复 `finding_alias`；adapter
  在本地审计 envelope 中把 alias 唯一映射回宿主 `finding_ref`，长 ref 不进入模型语义 payload；
- 四种 disposition 的 reason 均非空；`resolved`/`still_open`/`disputed` 提供的 evidence 必须能
  绑定当前 item revision，`insufficient_evidence` 可以没有 evidence 但必须说明缺少什么；
- 任何新 finding 都只引用当前 bundle，并重新经过第 10、12 节的 strict finding gate；
- context request 属于第 9.1 节白名单和本轮授权；
- disposition 中的 `finding_alias` 必须逐字回显宿主提供的短 alias；Pi 另行自选的 display ID、长
  hash、路径、自报 verdict 或 execution identity 不具权威性，均由宿主映射、忽略或拒绝。

复核通过后只提交一个 canonical `review-round-validated` composite event。外部结果版本引用第 8.2 节
current cache classification certificate，并在 payload 中同时内嵌唯一 attempt terminal/usage/settlement、
规范排序的 prior-finding disposition map、new finding/ref allocation、context request、derived verdict、
current work-unit/task/plan revision 和预期 ledger delta digest；cache attach 版本没有 attempt terminal，
但绑定 current classification generation、target alias revalidation 和零 usage。Event/referenced object
任一缺项都失败关闭。Reducer 以该单事件同时 terminalize attempt/accept request/更新整轮 ledger，SQLite
中逐 finding/attempt 行只是投影。
`finding-disposition-recorded` 若为兼容报表保留，只能是可删除/可重建的派生记录，不能作为另一套
事实事件。

因此进程在“第一个 finding 已处理”后崩溃不会产生半轮：canonical event 未提交则零项生效，已提交
则重放时全部生效。一个无效 disposition 令整轮 strict validation 失败；不能先提交其余合法项，
也不能靠后续 completion marker 猜测未提交的 disposition。

### 9.5 轮次终止与审核独立性

同一 model lineage 可以在新进程中复核自己的旧 findings，这属于 continuity review，用于提高
答辩效率，但不自动满足独立终审：

- 无 blocker/major/security，所有 finding 都有有效 disposition 且本地 gate 通过时可以结束；
- `resolved` 仍须绑定当前 revision 和本地验证，不能仅凭 reviewer 表态完成；
- blocker/major/security 候选按第 13.4 节使用独立 reviewer 或显式授权的
  `degraded-independence`；
- 通过 strict gate 的新 finding 只能引用当前 bundle。若当前 round 小于
  `max_continuity_rounds`，宿主分配新的稳定 `R-NNN`，归入当前 task 的下一轮并共享原上限，
  不覆盖旧 finding，也不重新获得三轮；
- 若问题需要当前 bundle/task 外内容，它只能先成为受控 context request 或 scope drift；重新 plan、
  授权后才可建立新 task。不能仅凭 Pi 的 new finding 文本直接创建 task 或重置轮次预算。

最后一个允许 continuity round 使用唯一 reducer，不再写“`disputed` 或 `escalated`”这样的可选分支：

| validated Pi status | finding/campaign 动作 |
|---|---|
| `resolved` | 进入本地 validation；低风险 gate 全过则 `verified`，高风险则 `independent-final-required` |
| `still_open` | finding 进入 `awaiting-terminal-disposition(reason=still-open-at-limit)` |
| `disputed` | finding 保留 Pi status=`disputed`，进入 `awaiting-terminal-disposition(reason=reviewer-disputed)` |
| `insufficient_evidence` | finding 进入 `awaiting-terminal-disposition(reason=evidence-exhausted)` |
| 任意 `new_finding` | 分配稳定 ref 后进入 `awaiting-terminal-disposition(reason=new-at-limit)` |

只要存在后一类状态，task 进入同名非 terminal 状态并禁止新的 provider attempt，但不能先
`task-escalated` 再允许本地 disposition。主代理/用户必须在 task terminal 前逐项执行
`finding-dispose`：`false-positive` 和有效 `waive` 可关闭当前 campaign 的责任；`accept` 只表示承认，
必须在同一 finding event 中绑定预先存在的 follow-up responsibility；`escalate` 同样绑定 successor
或明确人工 owner。全部 finding 均为 verified/false-positive/有效 waiver 且其他 gate 通过时，task 才能成功
terminal；任一 accepted/escalated/disputed/insufficient 项则 task 确定进入 `task-escalated`，campaign
按 drain barrier 进入 `terminated-escalated`。没有处置时 campaign 明确保持待决，不伪装完成。

Follow-up 不声称能与另一个 event file 跨链原子创建。执行 `accept`/`escalate` 前必须先得到以下之一：

- maintenance chain 中已 commit 的 `campaign-requested(purpose=terminal-finding-follow-up)`，其 immutable
  payload 绑定 source campaign、work-unit instance、finding ref/key、current revision、reason、owner/
  requested SLA 和 idempotency key；后续 campaign genesis 可由该 request 确定创建；
- 已存在且 genesis 明确引用上述 source facts 的 successor campaign；
- maintenance chain 中已 commit 的 `manual-follow-up-owned` assignment，绑定明确 owner、责任范围、
  复检条件和 authority。

`finding-dispose` 只引用这个已 durable 的 responsibility digest，并在一个 campaign event 内同时记录
finding `accepted|escalated`、current revision、authority 和责任绑定；引用不存在、source/revision 不
匹配或 owner 为空时拒绝。多个末轮 finding 可逐项绑定责任，但 task 在所有项都有 disposition 前保持
non-terminal；最后一次处置用一个 `terminal-disposition-committed` composite 固化完整 disposition map
并把 task 变为 escalated 或 success，避免先 terminal 再补 owner。高层 `audit drive` 可以先创建并
展示 follow-up request，再等待用户选择，不能在同一不透明命令中假装跨 maintenance/campaign chain
全成全败。

该规则同样适用于末轮 note 和绑定 context request 的 finding：round reducer 可能对 note-only 输出
给出 `approved`，但 campaign completion 仍被 `awaiting-terminal-disposition` 阻断。不得创建第四轮、
自动 waiver、在 task terminal 后补写 local accept，或因新 finding 更换 task 而重置预算。

独立终审不占用 continuity ordinal，也不叫“第四轮”。它使用单独的
`independent_final_review_generation`、`max_independent_final_reviews`（默认 1）和授权 stage/call/token
预算；transport retry 计 attempt/call，但不产生新的语义 generation。高风险 candidate 在授权/remaining
中没有独立终审名额时不得接受/应用；高风险 host revision 也不得提交
`bounded-host-revision-accepted` 或 `exact-host-revision-authorized-and-accepted`。必须先 reauthorize
或放弃该 campaign 派生路径。独立终审发现任何 new finding
或非 resolved disposition 时，先原子记录 final result，再进入上述 terminal-disposition/draining
流程；finding 通过新的
`terminal-finding-follow-up` campaign 处理；不能回到已耗尽的 continuity ordinal，也不能自动增加
第二次独立终审。这样 continuity 上限、独立门禁和 campaign 总调用上限各自可重建。

Round verdict 只描述本轮模型输出，不等于 campaign completion；`awaiting-terminal-disposition` 才是
末轮未决项的唯一宿主状态。这样既保留 note 非 actionable 的语义，也不会把没有复核机会的新 note
静默丢弃。

因此，规范实现不需要 Pi RPC bridge。未来若为非本仓库场景提供持久 session，它必须是明确标记的
interactive/unsafe 工具，不能接入本方案的 canonical review、cache、authorization 或 completion
gate。

## 10. 模型输出契约适配

模型不再负责返回 schema_version、contract、bundle_id、长 item_id 或绝对路径。
初审时 Pi 只返回以下受约束 payload。答辩复核使用第 9.4 节的 disposition payload；额外 remediation
使用第 13.3 节独立的 `tome4-remediation-result-v1`，不能把候选生成输出伪装成 review disposition。

```json
{
  "findings": [
    {
      "primary_alias": "i03",
      "severity": "major",
      "category": "code",
      "title": "...",
      "body": "...",
      "confidence": "high",
      "evidence": [
        {
          "item_alias": "i03",
          "anchor": "hunk:h03:line+4",
          "claim": "该分支使授权集合外的 revision 被复用",
          "rule_id": "authorization-derived-revision"
        },
        {
          "item_alias": "i08",
          "anchor": "hunk:h08:line+2",
          "claim": "第二个入口沿用同一未经授权的 revision。",
          "rule_id": "authorization-derived-revision"
        }
      ],
      "candidate": {
        "action": "patch-group",
        "members": [
          {
            "path_alias": "p01",
            "action": "patch-code",
            "patch": "..."
          },
          {
            "path_alias": "p02",
            "action": "patch-code",
            "patch": "..."
          }
        ]
      }
    }
  ],
  "context_requests": []
}
```

本地 adapter 负责：

- 注入不可变 envelope；
- 将每条 evidence 的 `item_alias` 分别映射回 item ID/revision；可选 `primary_alias` 只用于展示和
  task 路由，必须指向某条 evidence，但不参与 finding 身份；
- 规范化并校验每条 evidence 的 item/anchor/member anchor，聚合生成稳定 finding key；
- 对 occurrence group 的 member 级 finding 强制要求 `member_anchor`；alias 或行号不能代替成员身份；
- 将 `path_alias` 映射回当前 bundle 中已授权的公开路径，把单/多 member 输出规范化为第 13.2 节
  的 candidate group，并由宿主生成 member/group digest 与规范顺序；
- 校验 severity、category、confidence、candidate action、per-file base revision 和 group 原子性；
- 拒绝未知 alias、越界路径或未绑定 revision；
- 对缺少 envelope 等确定性错误进行本地规范化，而不是重新付费调用。

`strict` 同时作用于两个独立 gate：

- finding strict validation：无法唯一绑定 alias/item/member/revision/evidence 的输出进入
  `quarantined-unstable`，不成为 finding；基线整份 review payload 失败关闭，不能把其余 finding
  部分提交后假装 coverage 完整；
- candidate strict validation：拒绝无法唯一绑定 base revision、finding、路径、hunk 或 action 的
  候选，并禁止它进入 `candidate-validated` 或派生链。

candidate gate 失败不应丢弃已经严格验证的 finding；候选记录为 `rejected`，或在含 redacted
literal 时按第 13.5 节降级为 `parameterized-advice`。宽松模式只能补齐确定性 envelope，不能猜测
item、member、路径、revision、patch 内容或参数绑定。CLI 的 `--strict` 默认同时启用两个 gate；
如内部测试单独调用 gate，也必须在最终 campaign completion 前同时通过。

## 11. Planner 与分包

### 11.1 风险优先级

Planner 在调用 Pi 前先运行本地确定性检查：

- 代码 diff、测试失败、路径和 schema 检查；
- 翻译 printf、控制标记、术语、空译文和运行键检查；
- 已知 finding waiver 与当前 revision 匹配检查，并将到期/到达复检时间的 waiver 重新排入任务；
- 当前 task revision 集合与授权/派生集合的 scope drift 检查。

建议风险层级：

- P0：blocker/security、失败关闭边界、数据泄露、构建阻断；
- P1：修改过的接口、复杂状态流、格式/标记警告、待审术语；
- P2：普通改动与周期性抽样；
- P3：未变化且已有精确审核缓存的内容。

高 reasoning 模型优先用于 P0/P1。P2 可使用较低 thinking 或抽样策略。

### 11.2 Token 预算与语义分组

- 分包以估算 token 为主，不以固定条目或文件数量为主。
- 代码按模块、调用关系和测试关系分组；相关实现与测试尽量同包。
- 翻译按 component、section、source_tag 和术语上下文分组。
- 单个超长条目必须单独成包，超过硬限制时暂停并报告，不得静默截断。
- Bundle 记录 kind、估算输入/输出 token、estimator version、条目数和分组原因。

## 12. Finding Ledger

Finding 由本地生成稳定 key。模型标题不参与身份，公式为：

```text
evidence_record_fingerprint = H("finding-evidence-record-v2", {
  rule_id_or_category,
  item_id,
  item_revision_hash,
  canonical_item_relative_anchor,
  member_anchor_or_null,
  normalized_claim
})

evidence_fingerprint = H("finding-evidence-set-v2", {
  finding_canonicalization_version,
  canonical_sorted_unique_evidence_record_fingerprints
})

finding_key = H("finding-v2", {
  category,
  evidence_fingerprint
})
```

`finding_key` 是 revision-bound 的机器身份，不适合作为多轮对话中的人类编号。宿主为 campaign
中的每个逻辑问题分配单调、不可复用的 `finding_ref`（例如 `R-001`），并以
`review-round-validated.finding_ref_assignments` 原子子记录保存 allocator version、finding key 和
round；不能先提交独立 ref event 再提交整轮 result。手工 import 也由单一 composite import event 同时
分配 ref。Pi 输出中的自选编号只作
临时 alias，不能成为权威引用；新增 finding 通过 strict gate 后才由宿主分配下一个编号。

同一问题跨 revision 延续时保留 `finding_ref`，但生成新的 `finding_key`，并用 `continuation_of`、
`supersedes` 和可选 `finding_family_id` 显式连接版本。只有上一轮 disposition 对同一
`finding_ref` 返回 `still_open`，或宿主能够由已接受 candidate/精确 revision 因果链证明延续关系时
才能连接；不得仅凭相似标题或自然语言自动合并。Pi 报告的 `new_findings` 始终先按新问题处理，
除非本地 validator 能以确定性旧 key/ref 证明它只是重复项。

`canonical_item_relative_anchor` 必须由宿主把每条 evidence 的 item alias/hunk/entry anchor 解析成
bundle 内的稳定相对位置；跨 item finding 的每条证据各自绑定 item ID、该 item 的 revision 和可选
member anchor。`primary_alias` 只作展示/路由提示，不能替代任一证据绑定，也不进入 identity。

Finding 归属也不能由 `primary_alias` 决定。每个 open finding 有且只有一个 canonical
`owner_work_unit_instance_id`，其 `evidence_item_set` 必须被该 work-unit instance 完整覆盖。Planner 默认把一个跨 item
finding 的全部 evidence closure 保持在同一 task，直到 finding terminal；不得为了 token packing 把
它复制到两个 successor，或只把 primary item 迁走。若 token hard limit 迫使拆分，planner 创建一个
确定性的 aggregate finding-resolution task，只携带各 successor 的最小有界 evidence slice，并把
successor task 设为 dependency；finding 仍只归 aggregate task，不能共同拥有。

任何 task split/merge/delete 的 `task-lineage-replaced` payload 必须在同一原子 generation map 中，
以第 6.1 节严格递增的 work-unit instance edge 为每个 finding 指定唯一 successor/aggregate owner，
并证明新 owner 覆盖全部 evidence items。缺项、
重复 owner、跨两个 bundle 的部分 disposition 或试图复制 finding 都令 generation 失败关闭。跨文件
candidate 仍可原子绑定该 finding；所有 member 应用/复审完成前 owner 不迁移到单个文件 task。
`normalized_claim` 只做由 `finding_canonicalization_version` 定义的空白和标点规范化，不使用可变
标题。多条 evidence 去重后按 record fingerprint 规范排序再聚合；重复 record、缺少可验证
item/revision/anchor/claim 或 rule/category 时不得猜测合并，也不得进入 validated Finding Ledger。
任一被证据引用的 item revision 或 member anchor 变化都会产生新的 key。Adapter 把该输出放入独立的
`quarantined-unstable` store，当前 round 的 strict finding gate 失败；只有授权/预算允许时可走
payload repair，否则 task 保持 failed/needs-payload-repair。Quarantine 不参与 verdict、finding
coverage 或 completion。

Quarantine identity 使用可识别且版本化的稳定前缀，不能与正常 finding key 混淆：

```text
unstable_finding_key = "unstable-v1:" + H("quarantined-finding-v1", {
  attempt_id,
  output_ordinal,
  alias_or_missing_sentinel,
  canonical_raw_finding_payload_digest
})
```

同一 raw payload/attempt 重放时得到同一 quarantine key；不同 attempt 仍故意得到不同 key，避免在
缺少稳定 evidence 时跨执行误合并。`unstable-v1:` 对象不分配 `finding_ref`，不得参与自动去重、
continuation、waiver、候选绑定、disposition 或 verified completion。人工若认为内容有价值，必须在
当前有界公开输入上补出可验证 item/revision/anchor，并通过显式 `finding-imported-from-quarantine`
事件重新走 strict gate；新 finding key 不继承 quarantine 身份。

任一证据绑定 item 的内容改变后产生新的 finding key；旧 finding 通过显式 `superseded_by` 关系关闭。

Ledger 至少记录：

- campaign/task/work-unit instance/bundle/revision、`owner_work_unit_instance_id` 和完整 `evidence_item_set`；
- `finding_ref`、当前 `finding_key`、可选 `finding_family_id` 和跨 revision 关系；
- severity、category、evidence 和 confidence；
- candidate 及其验证结果；
- 每轮 Codex `stance`、reply digest、Pi disposition status/reason 和 reviewed revision；
- disposition：`open`、`accepted`、`false-positive`、`waived`、`fixed`、`verified`、`escalated`、
  `superseded`，以及非 terminal 的 `awaiting-terminal-disposition`；
- 对 `accepted`/`escalated` 必填的 follow-up responsibility digest、successor/manual owner 和 source
  maintenance event；
- 应用 revision 和最终验证结果。

Codex `stance`、Pi round `status` 和 ledger `disposition` 是三个不同字段，不能相互覆盖：

```text
open
  → Codex: fixed | partially_fixed | disputed | needs_context | accepted_not_fixed
  → Pi: resolved | still_open | disputed | insufficient_evidence
  → 宿主: verified | open | awaiting-terminal-disposition | waived | escalated | superseded
```

例如 Pi 返回 `resolved` 只允许宿主在当前 revision、本地 validation 和适用的独立复审 gate 均通过
后写入 `verified`；Pi 返回 `still_open` 则创建或关联当前 revision 的 finding key，并保持同一
`finding_ref`。达到轮次上限的分歧先写入 `awaiting-terminal-disposition`，只有第 9.5 节的显式
authority action 后才成为 `false-positive`、`waived` 或 `escalated`；不能由 reducer 任意选择终态。

`superseded` 不是通用清理状态，必须记录受控 reason 和 source event：revision 正常更新使用
`revision-replaced`；精确派生删除使用 `authorized-derived-removal`。task 意外消失时 open finding
保持 open 并触发 scope drift；用户决定缩小范围时由 campaign cancellation/supersession event
处理，不能靠批量写 `superseded` 让旧 campaign 通过 completion gate。

`false-positive` 与 `waived` 只绑定当前 item revision。waiver 必须记录 reason、approver、
`created_at`、`expires_at` 与 `next_review_at`：note/minor 默认最长 90 天，major 默认最长 30 天；
blocker/security 不提供默认 waiver，只有用户显式批准时才允许创建，且默认最长 7 天。到期或
到达复检时间的 waiver 在 active campaign 中重新进入 planner，不能计入 campaign 完成条件；
已完成 campaign 按下段创建新的 maintenance campaign。

内容变化后，active campaign 中的 `false-positive` 和 waiver 自动重新打开；已完成 campaign 由
新 campaign 处理。未变化的 false-positive 仍进入周期性抽样复检；默认每 90 天按 category 至少
抽 1 条、最多抽该类 5%，避免永久静默。需要跨 revision 沿用的判断必须提升为显式 policy，并由
用户或维护者批准、版本化和审计。

已完成 campaign 保持不可变，不因 30/90 天计时器重新打开。waiver 到期、`next_review_at` 到达或
false-positive 周期抽样时，maintenance planner 创建新 campaign，引用原 campaign/finding/revision，
使用最新 policy、校准 snapshot 和新授权。为避免精确缓存把周期复检变成空操作，该 task 使用受
审计的 `--force --reason waiver-expiry|false-positive-sample`；它仍计入新 campaign 的调用与 token
预算。若原 campaign 尚未完成就到期，则 waiver 当场失效并恢复为 open。

## 13. 候选修订与验证

### 13.1 翻译候选

`replace-translation` 必须转换为现有 proposal 结构，并经过：

- source/source_tag/workset 身份校验；
- candidate member digest、finding、base plan/file/entry revision 及 file mode/type 绑定；
- printf 参数及 args_order 校验；
- 控制标记和术语校验；
- LuaJIT 加载与普通 lint；
- 应用后受影响条目的增量复审。

单条翻译 proposal 也包装成单 member candidate group，从而与第 6.3 节使用同一排序、授权和
原子应用契约。
其跨 campaign `semantic_candidate_effect_digest` 同样只覆盖 stable component/section/source/source_tag/
entry base revision、action 和 exact target/proposal bytes，不包含 campaign、plan instance、finding ref 或
author；target attach 再生成本地 group/provenance。不能让翻译候选重新引入第 13.2 节已排除的本地身份。

### 13.2 代码候选

跨文件修复使用原子 candidate group，而不是一个缺少 per-file revision 的多文件 patch。group
至少记录 `base_plan_revision_id`、绑定 finding keys、author execution fingerprint、规范 member
列表和 `candidate_group_digest`。每个 `patch-code` member 只能修改一个公开文件，并绑定：

- 公开相对路径；
- 相关 `item_id/base_item_revision` pairs、该文件的 `base_file_revision_hash`、`base_file_mode_and_type` 和
  `expected_file_mode_and_type`（默认仍为相同 mode 的 single-link regular file；只有显式
  `delete-code` action 可为 `absent`，并走第 6.3 节受控 scope contraction）；
- 最小 unified diff/hunk；
- 一个或多个 finding keys；
- action、contract version 和 `candidate_member_digest`。

```text
semantic_candidate_member_effect_digest = H("semantic-candidate-member-effect-v1", {
  candidate_contract_version,
  action,
  canonical_public_path,
  base_file_revision_hash,
  base_file_mode_and_type,
  expected_file_mode_and_type,
  ordered_item_base_revision_pairs,
  exact_patch_bytes
})

candidate_member_digest = H("candidate-member-v3", {
  semantic_candidate_member_effect_digest,
  ordered_finding_keys,
  local_alias_binding_digest
})

member_order_key = (
  canonical_public_path_bytes
  minimum_finding_key
  candidate_member_digest
)

semantic_candidate_effect_digest = H("semantic-candidate-effect-v2", {
  canonical_sorted_semantic_candidate_member_effect_digests
})

candidate_instance_effect_digest = H("candidate-instance-effect-v2", {
  base_plan_revision_id,
  ordered_candidate_member_digests
})

candidate_group_digest = H("candidate-group-v4", {
  candidate_instance_effect_digest,
  author_execution_fingerprint
})
```

member 按 `member_order_key` 规范排序，同一路径在一个 group 或同一 generation 的 accepted groups
中最多出现一次。一个 member 可包含同文件内多个已合并 hunk 并绑定多个 finding；宿主不得擅自
语义合并两个模型 patch。重复路径、重叠 hunk 或不同 base revision 必须拒绝，改由 provider 产生
一个合并 group，或在应用并复审后的下一 generation 重新生成候选。

上述 `ordered_item_base_revision_pairs` 和 `ordered_finding_keys` 均按规范 bytes 排序；前者把稳定
item ID 绑定到其 base revision，不能只复制 campaign-local alias。`exact_patch_bytes` 只做
candidate contract 声明的 UTF-8/LF 规范化，不做 formatter 或模糊 patch 重写。

`semantic_candidate_effect_digest` 只描述跨 campaign 可比较的规范修改：它不含 campaign、plan
instance、finding ref/key、local alias 或 author provenance，成员按 `(canonical path bytes,
semantic member digest)` 独立规范排序。全局 cache equivalence 只使用该 digest；两个 attempt 产生
相同 effect 不会仅因 campaign-local `base_plan_revision_id` 或 author identity 不同就被判为 conflict。
`candidate_instance_effect_digest`/`candidate_group_digest` 则绑定 target campaign 的 base plan、finding
映射和实际 author provenance，用于本地接受链与独立性，不能反向进入跨 campaign decision projection。

Cache attach 遇到 candidate 时，adapter 先用 target current files/items 重算 semantic member/effect
digest并与 source observation 完全匹配，再物化一个新的 target-local candidate group：它使用 target
`base_plan_revision_id`、target finding bindings 和 source 的真实 author execution provenance，生成新的
instance/group digest。来源 campaign 的 local candidate group 不能直接复制；映射失败、base revision
不同或 semantic digest 不同则该 observation 对 target 不可 attach，而不是制造伪 conflict。

group 级 finding keys 必须精确等于所有 member finding keys 的规范并集，不得另有未进 digest 的
绑定；`primary_finding_key` 是该并集的规范最小值。group 按第 6.3 节的
`(primary_finding_key, candidate_group_digest)` 排序。group 内所有路径必须同时位于 campaign 本地
allowlist 并已作为 current task/item 提供 base file revision；只作为补充 evidence 出现的文件不能直接
成为 candidate target，除非先重新 plan 把它提升为受审 task，并在需要外发时纳入 external
authorization。跨文件 group 必须在临时副本中全量
校验并原子应用：任一 member 失败、越界或 revision 不匹配，整个 group 均不得进入 accepted
列表，不能部分应用。

宿主先在临时副本中检查 patch 可应用性、路径边界和相关测试。测试通过只代表候选可供
主代理判断，不代表自动授权写入共享工作区。临时副本与真实应用都必须禁用 formatter 和修改型
hook；应用后立即计算 expected/actual canonical revision，运行只读测试后再次计算。任何测试、
lint 或 hook 造成的 canonical 内容、mode、type 或 link count 变化都使候选失去派生资格并触发新 plan。

Candidate 的可达闭环固定为：

```text
reviewed/needs-fix
  → audit validate (candidate-validated)
  → audit candidate-accept (candidate-generation-accepted / candidate-accepted)
  → 主代理在共享工作区应用
  → audit record-applied (applied + new plan/task revision)
  → audit prepare-round/respond (current-revision codex-response-recorded)
  → review-reply 或 independent-final
  → audit verify
```

`audit candidate-accept` 必须接收完整、规范排序的 group generation 与主代理 authority，一次原子固化
base plan、expected revision set、finding 并集和下一 plan revision；不能逐 group 接受后留下半代。
`audit record-applied` 只接受该 current accepted generation，且工作区 actual canonical revision set
必须与 expected 全等。`audit validate` 不拥有 accept 权，`record-applied` 不隐式补 accept，reply 也
不能先于 applied revision。无 candidate 的人工修订改走第 6.3 节 bounded 或一次性 exact host
acceptance，不伪造 candidate author 或 group digest。

### 13.3 Campaign remediation

额外 remediation 是 campaign 内受预算约束的候选生成 stage，不是绕过 ledger 的低层捷径。只有第 5.1
节的明确触发条件成立、current work-unit/finding 尚未 terminal、授权包含 `stage=remediation` 且对应
lineage entitlement/预算仍可达时，planner 才能创建实例；默认每个 lineage 最多 1 个 semantic
remediation request。它不能自行读取工作区、修改文件、关闭 finding 或复述一个自报的“已解决”
verdict。

身份与冻结输入为：

```text
remediation_instance_id = H("remediation-instance-v1", {
  campaign_id,
  owner_work_unit_instance_id,
  current_plan_revision_id,
  current_task_revision_id,
  ordered_target_finding_keys,
  basis_validated_review_digest,
  accepted_evidence_digest,
  remediation_generation
})

remediation_request_instance_id = H("remediation-request-instance-v1", {
  remediation_instance_id,
  observation_generation,
  payload_repair_generation,
  prompt_digest,
  contract_version,
  decode_config_digest
})

remediation_result_cache_key = H("validated-remediation-result-cache-v1", {
  exact_remediation_semantic_payload_digest,
  prompt_digest,
  contract_version,
  redaction_version,
  provider,
  resolved_deployment_id,
  model_lineage_id,
  thinking,
  validator_version,
  decode_config_digest
})
```

Model semantic payload 只含 current bounded public content、目标 finding 的规范 evidence/resolution
condition、已接受的公开 evidence、候选合同和允许 action；campaign/work-unit/ref/authorization/预算等
只在 local envelope。输出 `tome4-remediation-result-v1` 只允许：绑定每个 finding/item/base revision 的
candidate group、`parameterized-advice` 或带 reason 的 `no-change`。它不含 finding disposition；未知
alias、越界 path、旧 revision、部分跨文件 group 或自报 applied/verified 均 strict 拒绝。

状态机固定为：

```text
remediation-required
  → remediation-planned
  → remediation-cache-checking
       ├─ eligible cache hit → remediation-result-validated
       └─ miss → awaiting-external-authorization
                 → remediation-running
                 → remediation-result-validated
                      ├─ candidate payload → candidate-validated
                      │    → candidate-generation-accepted → applied → reply → re-review/final
                      ├─ parameterized-advice → host-action-required
                      └─ no-change → host-action-required | terminal disposition
```

Remediation 使用第 8.2 节同一套 per-key lock、singleflight、classification generation 和跨链 pending
saga；其 key 使用独立 domain，不能与 review result 混用。Strict validated 外部结果由单一
`remediation-result-validated` campaign composite 同时 terminalize attempt、结算 usage/slot、接受唯一
request result 并记录 candidate/advice/no-change；不能先写 `attempt-completed`。Cache hit 仍须在 target
base revision 上重验，并按第 13.2 节由 campaign-neutral semantic effect 重新物化 target-local group。
两个非等价 remediation results 同样触发 conflict，不得任选较新的 patch。

有效 candidate 接入既有 `candidate-validated → candidate-generation-accepted` authority gate；
remediation validator 没有 accept/apply 权。Candidate 的 `author_execution_fingerprint` 必须来自实际
remediation attempt（cache attach 时保留 source author provenance），并加入
`remediation_influence_execution_fingerprints`；后续 high-risk final reviewer 必须与所有影响执行满足
独立性 predicate。主代理若只采纳 parameterized advice 形成 byte-different host fix，也必须走 bounded
或一次性 exact host acceptance，并把该 remediation execution 记录为 influence。

低层 `tools/pi-remediate --bundle ... --review ...` 只能由 campaign runner 在上述 planned request、
authorization、concurrency slot、reservation 和 no-tools/no-session 边界齐备后调用；直接运行产生的
artifact 没有 canonical campaign 资格。高层入口为 `audit plan-remediation` 与
`audit run --stage remediation`，`audit drive` 只在触发条件与 frozen stage graph 均满足时自动规划，
不会替用户扩 stage/预算或应用输出。Remediation 的 normal attempt、transport retry、payload repair
和 force 全部进入第 5.2 节最坏调用预览；lineage split/merge 不复制其 remaining entitlement。

### 13.4 独立复审 gate

候选作者由宿主根据 `stage + provider + resolved_deployment_id + model_lineage_id +
model_alias_mapping_digest + thinking + prompt_digest + attempt identity + semantic request context digest`
生成并签入 envelope 的 execution
fingerprint，不能接受模型自报身份。应用后的最终复审必须
使用新的 bundle revision 和新的 review request instance；note/minor 的普通增量复审可按第 8.2 节
命中未冲突语义 cache，major/blocker/security 则必须按下文 fresh-only 规则创建新的外部 attempt。
不得把候选作者的自检、同一响应中的“修复后无问题”或本地测试当作最终审核。

```text
execution_fingerprint = H("model-execution-v3", {
  stage,
  provider,
  resolved_deployment_id,
  model_lineage_id,
  model_alias_mapping_digest,
  thinking,
  prompt_digest,
  attempt_id,
  semantic_request_context_digest
})
```

Review 的 `semantic_request_context_digest` 取第 8.2 节 `semantic_round_context_digest`；remediation 则取
第 13.3 节冻结 finding/evidence/base revision payload 的 context digest。两者不能只因字段名不同而
遗漏 influence，也不能把 local campaign envelope 混入 semantic context。

Execution fingerprint 用于证明“这是不同输入/attempt 的执行”，不是独立性的充分条件。不同 round
context 会产生不同 fingerprint，但两个别名若解析到同一 model lineage，或同一 lineage 对
自己旧 finding 做 continuity review，仍不因此成为独立终审。独立性 predicate 必须另外检查全部
remediation influence executions（candidate author 及被 host fix 采纳的 finding/advice reviewer）、
provider security boundary、`resolved_deployment_id`、`model_lineage_id`、thinking、prompt、
无 session 边界和用户授权；实现不得简化为 `reviewer_fingerprint != author_fingerprint` 或比较 alias 字符串。

每次外发前，provider adapter 必须用授权中冻结的 alias mapping snapshot 把名称解析成
provider-qualified immutable deployment identity 和 canonical underlying model lineage，提交
`model-resolution-recorded`，并把 `resolved_deployment_id`/`model_lineage_id` 写入
`attempt-started`、结果 envelope 和 cache key。Provider 回执若提供实际 serving identity，必须与
冻结 identity/允许的兼容集合匹配；漂移时结果 stale、campaign 暂停。不同 provider/deployment 若
指向同一 known lineage，仍不满足“不同模型”的默认独立性。
无法取得可验证 lineage 的模型可以做普通 continuity review，但默认不能满足独立终审；只有用户
针对该不确定性显式授权 `degraded-independence`，并在报告中保留 resolver/mapping digest 与风险理由，
才可作为降级门禁。换 alias、换 endpoint 名称或更新 mapping digest 都不会自动创造独立性。

- note/minor：允许同一次初审附带候选；主代理接受并应用、测试通过后，再做普通增量复审；
- major/blocker/security：最终复审者不得是候选作者，默认使用不同且可验证的 model lineage；
- 只有用户明确授权时，才允许同模型以独立 prompt、无共享 session 和不同 thinking 作为降级
  复审，并在完成报告中保留 `degraded-independence`；
- 独立复审所需的 provider/model 若未在初始授权中列出，必须在外发前追加授权；
- 任何复审发现新问题都会创建新 finding，不能覆盖原 finding 或自动延长 waiver。

独立终审不是预算名词，而是完整状态机。对每个含 major/blocker/security candidate 的 current task
revision，宿主确定性生成：

```text
independent_final_instance_id = H("independent-final-instance-v2", {
  campaign_id,
  work_unit_instance_id,
  task_id,
  current_plan_revision_id,
  current_task_revision_id,
  remediation_generation_digest,
  ordered_remediation_influence_execution_fingerprints,
  host_authority_digest_or_null,
  independent_final_review_generation
})

independent-final-required
  → independent-final-planned
  → independent-final-running
  → independent-final-validated
  → independent-final-passed | awaiting-terminal-disposition
```

`remediation_generation_digest` 可以引用 accepted candidate generation、bounded host revision 或
一次性 exact host revision；纯 host revision 没有 candidate author fingerprint，但保留 host authority。
Influence set 至少包含 initial/candidate/remediation author，以及生成被 host fix 采纳之 finding/advice 的
reviewer/remediator execution；最终 reviewer 默认不得与其中任一项
共享 model lineage。`independent-final-planned` 必须同时冻结 final instance、最新 applied bundle、
需要复核的全部高风险 finding、influence fingerprints/host authority、规定的只读测试证明、独立
reviewer mapping 和 authorization。
本地 independence predicate 在 attempt 前和 result 后各检查一次。Transport retry 复用该 final
instance/request，按第 9.3 节严格串行；payload repair 只增加 request generation；二者都不增加
`independent_final_review_generation`。默认 generation 上限为 1。
`independent-final-validated` 与第 8.1、9.4 节一样，在单一 event 中原子携带 attempt terminal/settlement、
cache classification certificate、完整 disposition/new finding/context request/ref allocation 和 ledger
delta，不能先 terminalize attempt 或逐 finding 提交。

独立终审采用 `fresh-execution-required`：普通跨 campaign/result cache hit 不能满足 gate，即使内容
相同；否则“新的独立执行”会退化为历史结果复用。唯一不重复外发的恢复场景是同一 final instance、
同一 `attempt_id` 已有 canonical validated terminal/CAS object，但进程在 ledger 投影前崩溃，此时只
重放既有 event，不叫 cache attach。该选择牺牲少量高风险缓存收益，换取可证明的独立性；低风险
普通增量复审仍可使用语义 cache。

Final validator 要求每个目标 high-risk finding 恰有一个 `resolved` disposition，当前 revision/local
tests 仍匹配、result key 未处于 unresolved conflict，且没有任何 new finding/context request。全部满足才提交
`independent-final-passed`；`still_open`、`disputed`、`insufficient_evidence`、任意 new finding、
serving identity drift 或 independence predicate 失败都原子进入第 9.5 节
`awaiting-terminal-disposition`，不能回到 continuity、重跑第二个 final generation 或任选缓存结果。
`audit plan-final`/`audit run --stage final-review` 是低层入口，`audit drive` 可在 prerequisites 满足时
自动规划；两者都受同一事件与预算契约。

### 13.5 Redaction

不再用单一正则把所有绝对路径替换为无语义占位符。使用类型化 redaction：

- `<repo-root>/relative/path`
- `<home>/relative/path`
- `<external-repo>/<logical-name>`

受保护 root、其路径或其内容不做 outbound redaction 后继续发送，而是在 payload 构建阶段直接
拒绝；本地失败记录只能保留已声明 component 和错误类别。其余外发内容不包含反向映射。
redaction adapter 在本地保留不可外发的 typed span/taint 元数据，用来判断候选是否依赖占位符，
不能仅凭字符串正则猜测。

candidate group 任一 member 的路径 header、增加/删除行或上下文行只要包含 redacted/tainted
literal，candidate gate 就必须把整个原子 group 降级为 `parameterized-advice`，不能拆出其余
member 部分接受。参数化候选永不进入 accepted candidate 列表，也不进入第 6.3 节的 candidate
group 派生链；Phase 1–3 基线不做自动反向替换。主代理
依据建议对真实公开内容作出的任何修改都是新的 plan 输入，必须重新计算 revision、执行 scope
检查；只有当前 external authorization 已明确采用 `bounded-same-logical-scope` 且该修改通过
`bounded-host-revision-accepted` 全部上限/gate 时才可沿用外发授权；默认 exact 模式则必须提交
`exact-host-revision-authorized-and-accepted`，普通 reauthorize 不足以接入 plan。只有完全不依赖
redacted span、能在未脱敏 base revision 上原样严格应用的
候选，才可能进入派生链。redaction 只改变 outbound payload，不能反向参与 `revision_hash`。

## 14. 被临时忽略组件的工作流能力

单一 `addon_eligible` 不能表达“保留译文并 lint，但不提取、不构建、不发布、不外审”。
后续 manifest 应把组件能力显式拆分，例如：

```json
{
  "workflows": {
    "extract": false,
    "lint": true,
    "review": false,
    "build": false,
    "release": false
  }
}
```

当前暂时忽略的 `items-vault` 和 `possessors` 建议采用上述能力：保留规范译文和 lint，
但默认不进入 Pi 翻译 review。公开 manifest/config diff 仍可进入代码审核。

## 15. Artifact 隔离与保留

- 增加可注入的 artifact root；测试必须使用临时目录并在结束时清理。
- 真实 validated bundle、review、Codex reply、round disposition、finding 和 campaign event 长期保留。
- Raw model output 只有在超过 7 天、未被 active/failed campaign 或调查记录引用时才具备回收资格。
- `.aborted-pending/` 只保存无法成为 event 的 crash residue；恢复器记录其 expected event ID、失败阶段和
  去敏 checksum 后，超过 7 天且未被 incident 引用时可进入显式 GC manifest。Active `.pending/` 永不
  由通用 GC 触碰。
- 未引用 CAS object 只有在超过 30 天且完整引用扫描仍为 orphan 时才具备回收资格。
- Validated result、finding、授权记录、event chain 和仍被 campaign 引用的对象永不自动删除。
- `locks/`、event `.pending/`、当前 event heads、`state.sqlite3` 及其 WAL/SHM、active writer/attempt/
  cache-flight/provider-slot lease 引用的对象永不进入 GC manifest；lock/pending 文件即使看似陈旧也
  不能由 GC 删除，只能由第 8.1 节精确恢复器处理。
- 第一阶段不自动删除。`gc --dry-run` 先按统一锁顺序取得 `cas-reference.lock` shared，再取得
  maintenance chain lock/lease，扫描不可变 event chains 并生成 manifest；manifest 逐项记录相对路径、
  对象 digest、类型、大小、年龄、引用判定、扫描时各 chain head 和回收原因，并输出 digest 与预计
  回收空间。Dry-run 释放锁后 manifest 只是候选，不能证明 execute 时仍可删除。
- 真实回收只能使用 `gc --execute --manifest <digest>` 执行完全相同的 manifest；执行前重新检查
  artifact root 边界、文件类型、symlink、digest 和引用状态。Execute 必须先取得
  `cas-reference.lock` exclusive，等待所有已有 shared reference commits 结束，再取得 maintenance
  chain lock；在 exclusive 屏障内重扫全部 campaign/maintenance heads 和 CAS 引用，任一 manifest
  对象成为 live、对象/类型变化或 chain 校验失败时，在任何移动前整体停止。所有正常 CAS→event
  引用提交也必须先取得 shared 屏障，因此 execute 扫描后到隔离移动之间不会出现并发新引用。
- GC 已持有 exclusive barrier 时，禁止调用会再次申请 shared barrier 的通用 event commit。它使用
  专用 `maintenance_commit_under_exclusive_barrier`，验证当前 exclusive ownership 和 maintenance lock
  后在现有 exclusive scope 内完成 maintenance writer acquire/fencing、domain event、release，绝不再
  申请 shared barrier；没有该 capability 的调用失败关闭。`gc-started` 必须在首个移动前由该路径
  提交，`gc-completed`/`gc-aborted` 也走同一路径，消除锁升级自死锁。`gc-aborted` 只允许尚未移动
  任何对象，或 rollback 已证明全部恢复之后提交；不能用它掩盖部分隔离状态。
- `gc-started` 固化 transaction ID、完整有序 manifest、quarantine root 和 recovery policy。每个对象
  只在同一文件系统内以 digest/no-replace 原子 rename 到 transaction 专属隔离区，随后 fsync 并提交
  `gc-object-quarantined` progress event。若崩溃发生在 rename 与 progress event 之间，recover 根据
  source/quarantine 两侧的 exact type/digest 唯一补记；不得重新移动到不同目标或跳过校验。
- Event chain 中存在未完成 `gc-started` 时，所有新的 shared CAS reference commit 必须先失败并提示
  `audit gc --recover`，不能在部分 CAS 被移走后继续建立引用。Recover 重新取得 exclusive barrier 和
  maintenance lock，逐项验证 `source present | quarantine present` 的唯一状态后幂等继续；若两侧
  缺失、digest/type 不符或文件锁定则停止并请求人工处理。可选 rollback 也必须按逆序原子恢复并
  写 progress/completed event，不能静默丢弃半次 transaction。
- GC execute 只移入隔离区；永久删除需要独立 manifest、明确执行和同样的 progress/recovery 协议。
- 全局锁序唯一为 `CAS barrier → sorted cache-key/provider-slot resource locks → maintenance lock →
  sorted campaign locks`；不需要的层级可跳过。GC、recover、cache attach、candidate、usage/terminal
  event 和普通 writer 都不得反向取得。锁竞争只能等待/失败，不得通过删除 lock 文件、
  忽略 stale 判断或跳过引用重扫继续。
- Raw output 和 campaign 数据保持最小文件权限，不写入 Git。

## 16. 失败与重试策略

- 传输错误、provider 5xx、空连接或 timeout：当前 attempt 先 canonical terminal，再在同一冻结
  `review_request_instance_id` 下以新的 `attempt_id`/`transport_attempt_ordinal` 指数退避重试最多 1 次；
  两次不得并发，任一 validated 后不得再重试，也不消耗新的 continuity ordinal。
- 默认 `timeout_seconds=1200`，也是单 bundle 上限；任何更短值或 provider 特例都必须来自版本化
  policy 或显式参数并记录原因，不能由调用点悄悄改为 180 秒。timeout 写入 attempt 与 usage event，
  lease 必须额外覆盖 completion grace；timeout/lease expiry 本身均不自动释放预算 reservation。
- 缺少 envelope：本地确定性补齐，不重新调用。
- 未知 alias、越界路径或无法绑定 revision：先拒绝该 payload，不得猜测修正。只有授权对象显式
  允许 `payload-repair` stage 且仍有全部预算时，才允许对同一 task revision 发起最多一次修复请求。
  修复 prompt 只能包含原 bundle、公开的 validator error code/最小说明和允许的 alias/path contract，
  不得补入新证据、扩大路径或泄露本地真实映射。
- payload repair 是新的 provider 调用和 successor request，不是 transport retry：必须记录 parent
  request/attempt、`stage=payload-repair`、`payload_repair_generation=1`，因 prompt 改变而产生新的
  prompt digest/result cache key，
  并完整计入 `campaign_max_calls`、`run_max_calls`、输入/输出 token、费用和 timeout。未授权、次数
  已用或任一预算不足时直接保留原失败，不得外发。
- Transport retry 沿用同一 request/`result_cache_key`/`transport_config_key`，但使用新的
  `attempt_id`、lease 和 ordinal，并记录原因与费用；每次 retry 都必须重新通过预算准入并原子提交
  自己的 reservation，不得创建无法关联的新 run，也不得让晚到响应覆盖 request 的唯一 validated
  result 或返还上一 attempt 的保守 debit。
- `--force` 必须提供原因，且仍受 hard calls、启用的 hard token/cost 维度和授权有效期约束；它不能
  把 forecast 伪装成 hard，也不能绕过 certified bound；普通 campaign 的 forced total 为 0 时必须
  拒绝，不能只靠 remaining calls 推导许可。
- Hard token certified bound 大于 remaining 时返回并记录 `budget-admission-blocked`；p90/历史估算
  只用于 forecast 和 packing，不能通过调低系数制造准入。未运行 task 不能伪装成 cache hit、waived
  或 verified。
- 逻辑 scope、每 generation current bundle 数、campaign unique outbound payload 数和 calls 始终是
  hard gate；input/output token 与 cost 只在授权 mode 为 hard 时按第 6.3 节 reservation 阻断，
  forecast 只记录偏差，disabled 不参与。Plan-scoped gate 在 plan/replan/cache attach/run 前检查，
  hard attempt dimensions 只在 cache miss/`--force` 前 reservation。精确 cache hit 不要求 calls
  remaining 大于零，也不创建临时 reservation。Provider actual 超过 certified token/cost bound 时是
  `budget-integrity-failure` 并请求 drain 后终止 campaign；不能用其他维度余额、reauthorization 或事后“校正”
  合法化已经越过的 hard authorization。
- 第 6.3 节定义的任何 scope drift 都提交 `scope-drift-detected` event 并暂停 campaign，不能
  自动扩大 bundle。重新授权只解决外发 authority；还必须通过对应 plan-generation/scope-expansion、
  candidate、bounded host 或一次性 exact host accepted event，才能产生新的 current task set。

## 17. CLI 草案

以下是未实现的历史 CLI 草案，不是命令参考。当前 `tools/i18n --help` 不提供 `audit`
子命令，审核与实现均按 Paseo 角色路由执行：

```bash
python3 -B tools/i18n audit drive --scope code --purpose initial-change-review
python3 -B tools/i18n audit drive --campaign <id>
python3 -B tools/i18n audit plan --scope code --purpose initial-change-review --trigger-event-digest <digest>
python3 -B tools/i18n audit plan --scope translations --changed-since <commit> --purpose periodic-review --trigger-event-digest <digest>
python3 -B tools/i18n audit show --campaign <id>
python3 -B tools/i18n audit cache-check --campaign <id>
python3 -B tools/i18n audit cache-resolve --key <result-cache-key> --resolution <resolution.json> --authority <authority.json>
python3 -B tools/i18n audit authorize --campaign <id> --authorization <full-snapshot.json>
python3 -B tools/i18n audit reauthorize --campaign <id> --parent-authorization <id> --authorization <full-snapshot.json>
python3 -B tools/i18n audit run --campaign <id> --run-max-calls 8 --concurrency 2
python3 -B tools/i18n audit run --campaign <id> --work-unit <instance-id> --force --reason '<reason>'
python3 -B tools/i18n audit respond --campaign <id> --work-unit <instance-id> --responses <reply.json> [--supersedes <reply-digest>]
python3 -B tools/i18n audit evidence-attach --campaign <id> --work-unit <instance-id> --request <request-id> --evidence <evidence.json>
python3 -B tools/i18n audit evidence-accept --campaign <id> --work-unit <instance-id> --evidence <digest> --authority <authority.json>
python3 -B tools/i18n audit prepare-round --campaign <id> --work-unit <instance-id> --responses <reply.json> [--evidence <evidence.json>]
python3 -B tools/i18n audit plan-round --campaign <id> --work-unit <instance-id>
python3 -B tools/i18n audit run --campaign <id> --work-unit <instance-id> --stage review-reply
python3 -B tools/i18n audit follow-up-create --kind <campaign-request|manual-owner> --source-campaign <id> --work-unit <instance-id> --findings <refs.json> --owner <owner.json> --idempotency-key <key>
python3 -B tools/i18n audit finding-dispose --campaign <id> --finding R-001 --action <accept|false-positive|waive|escalate> --reason '<reason>' --authority <authority.json> [--follow-up-request <digest> | --successor-campaign <id> | --owner-assignment <digest>] [--expires-at <rfc3339> --next-review-at <rfc3339>]
python3 -B tools/i18n audit validate --campaign <id> [--candidate-generation <generation.json>]
python3 -B tools/i18n audit candidate-accept --campaign <id> --generation <generation.json> --authority <authority.json>
python3 -B tools/i18n audit record-applied --campaign <id> --candidate-generation <digest> --actual-revisions <revisions.json> --authority <authority.json>
python3 -B tools/i18n audit record-host-revision --campaign <id> --work-unit <instance-id> --mode bounded --base <revision> --actual-revisions <revisions.json> --finding-bindings <bindings.json> --authority <authority.json>
python3 -B tools/i18n audit accept-exact-host-revision --campaign <id> --work-unit <instance-id> [--parent-authorization <id>] --authorization <full-snapshot.json> --base <revision> --actual-revisions <revisions.json> --finding-bindings <bindings.json> --authority <authority.json>
python3 -B tools/i18n audit plan-remediation --campaign <id> --work-unit <instance-id> --findings <refs.json>
python3 -B tools/i18n audit run --campaign <id> --work-unit <instance-id> --stage remediation
python3 -B tools/i18n audit plan-final --campaign <id> --work-unit <instance-id>
python3 -B tools/i18n audit run --campaign <id> --work-unit <instance-id> --stage final-review
python3 -B tools/i18n audit task-terminate --campaign <id> --work-unit <instance-id> --outcome <waived|escalated|failed|cancelled|superseded> --reason '<reason>' --authority <authority.json> [--successor <instance-id>]
python3 -B tools/i18n audit campaign-terminate --campaign <id> --outcome <escalated|failed|cancelled> --reason '<reason>' --authority <authority.json>
python3 -B tools/i18n audit campaign-supersede --campaign <id> --successor <campaign-id> --reason '<reason>' --authority <authority.json>
python3 -B tools/i18n audit verify --campaign <id>
python3 -B tools/i18n audit recover --campaign <id>
python3 -B tools/i18n audit export --campaign <id>
python3 -B tools/i18n audit gc --dry-run
python3 -B tools/i18n audit gc --execute --manifest <digest>
python3 -B tools/i18n audit gc --recover --transaction <id> [--rollback]
```

`audit drive` 是效率优先的高层 orchestrator：一次调用完成 plan、本地检查、cache attach、empty/
cache-only completion 和所有当前可达的无外发转换；遇到没有 active flight 可等待的首次 cache miss 时输出唯一 immutable
authorization proposal 并暂停，遇到 candidate 应用或 terminal disposition 时输出明确 action，绝不
替用户确认或修改共享工作区。取得授权/主代理动作后再次 `drive --campaign` 从 event head 继续。
低层命令保留用于测试、诊断和精确控制，但默认用户不需要手工串联 `plan → cache-check → respond →
plan-round → verify`。

草案中的 `audit run` 原计划只在即将外发时要求 external-transfer authorization；该路径从未
成为当前入口。`tools/pi-review` 现为无副作用 tombstone，`tools/pi-remediate` 仅是 dormant
兼容消费者，两者都不能被本文草案提升为活跃审核或 canonical candidate 路径。
`audit recover` 只重放并验证 event chain、取得更大的 writer fencing token、重建 SQLite 投影，不调用
provider，也不猜测修补损坏的最终 event。它可以按第 8.1、8.2 节唯一 reducer 追加：pending event 的
no-replace 安装/隔离结论、过期 writer/attempt lease terminal、pre-transfer attempt+round cancel、
post-transfer abandon、validated classification→target composite、cache/provider slot flight 收尾，以及
termination draining 的 outer terminal；不能主动创建 retry/provider call、选择 finding disposition、
resolve cache class 或从截断 event 猜 payload。GC 的部分移动只由独立 `audit gc --recover` 处理。

`audit plan` 先确保 maintenance genesis/`campaign-requested`，再创建 `campaign-created` genesis、
绑定本地 policy 并创建 planned generation，不隐式授权；它随后可本地完成 empty-plan 或 cache check。即使
`plan_content_key` 相同，不同 purpose/parent/request-event/generation 仍可创建周期性或 follow-up campaign。
`audit authorize` 只接受用户确认过的完整 immutable snapshot；`audit reauthorize` 必须以当前
authorization 为 parent，重述所有 scope/model/stage/绝对累计 ceiling，stale parent、局部 patch、
“再加 N 次”或低于 finalized debit + active reservation 的上限均拒绝。两者写入的 authority object
和确认摘要必须进入 event，不从 shell 用户名或调用者身份猜测授权。
普通 `reauthorize` 只改变外发 authority，不会自动把 byte-different workspace revision 接入 plan；默认
exact 模式必须使用 `accept-exact-host-revision`，由一个 composite event 同时完成完整 reauthorization
和 exact plan acceptance。该命令不修改工作区，只验证调用前已经存在的 exact bytes。

`audit cache-check`/`drive` 先执行 plan/scope/local-policy 与精确 cache gate；cache hit 直接记录本地
命中，即使 calls remaining 为零或尚无 external authorization 也不创建 attempt。只有 miss/`--force`
或 fresh-only final/remediation review 且当前没有可等待的 active flight 时，才进入
`awaiting-external-authorization`；同 key flight 的等待者先 recheck/attach，不要求自己的外发授权。人工等待阶段不占
singleflight。随后由 `audit run` 在外发前重新检查 key，仍需调用时才取得 per-key flight，并同时检查
lineage entitlement、attempt-scoped
remaining、campaign/global provider concurrency cap，创建 provider-slot pending reservation 和数值
预算 reservation，再提交 `attempt-started`；费用 gate 启用但没有冻结价格依据时不得运行。等待同 key
flight 不付费；conflicted key 只允许 `cache-resolve` 或 fresh independent path，不能 attach。

`audit respond` 只校验并记录 `codex-review-reply-v2`，不调用 provider；它必须检查上一轮 review、
所有 open finding、当前 item revision、stance/change refs 和证据 anchor。冻结前再次调用时必须
显式提供 active reply digest，按 generation replace 并记录 supersession；冻结后拒绝原 round 更新。
`audit plan-round` 只生成并校验
`tome4-review-round-v2` bundle，也不调用 provider。只有后续显式 `audit run --stage review-reply`
才会在授权和预算 gate 后把该 bundle 发送给 Pi；validated disposition 由 runner 自动记录，无需
Codex 手工编辑 ledger。存在 evidence 时优先用 `audit prepare-round`，由一个复合 event 原子完成
evidence accept/new generation、reply validation 和 round freeze；任一子步骤失败均为零状态变化。

`audit candidate-accept` 是 validate 与 record-applied 之间不可省略的 authority gate；它一次接受完整
generation。`record-host-revision` 只在当前 authorization 明示 `bounded-same-logical-scope` 且所有
finding/scope/size/redaction/cumulative cap 通过时提交 `bounded-host-revision-accepted`；默认 exact 模式
则必须使用 `accept-exact-host-revision` 的单 event reauthorization+plan acceptance，普通 reauthorize
不能替代。
`audit plan-remediation` 冻结第 13.3 节 instance/request/payload，`run --stage remediation` 才能在
singleflight、authorization、entitlement、concurrency 和预算 gate 后调用低层 runner；validated
candidate 仍须走 `candidate-accept`，advice/no-change 不会关闭 finding。
`audit plan-final` 只为已应用高风险 generation 创建第 13.4 节 fresh-only final instance，不调用
provider；后续 `run --stage final-review` 才外发。

`audit validate` 只做本地 schema/envelope/finding/candidate gate、临时 candidate group 原子应用
和定向测试，成功时最多推进到 `candidate-validated`；它不调用 provider，也不修改规范 Lua、代码
或配置，仅写审计 artifact/event，更不能隐式提交 `candidate-generation-accepted`。
`audit verify` 重新计算已应用 revision、运行规定的只读 lint/test、核对已存在的最终复审 artifact
并执行 completion gate；它同样不调用 provider、不应用候选或修改受审源文件。只有当前 task 因内容
应用、reply/evidence 或 high-risk policy 确实要求后续 review、且对应 artifact 缺失时，才返回
`re-review-required`；初审 clean task 不凭空要求第二轮。所需复审由后续已授权的 `audit run` 执行，再重新
`audit verify`。

`finding-dispose`、`task-terminate`、`campaign-terminate` 和 `campaign-supersede` 是第 6.2、12 节控制
event 的唯一 CLI 入口；它们要求非空 reason、版本化 authority/approver、当前 revision、受影响
finding refs 和适用 successor，不调用 provider、不改工作区，也不能把 escalation/cancellation 伪装
成 successful completion。存在 active attempt/round/reservation 时 terminate 命令只提交
`termination-requested` 并进入 draining；recover/drive 结算全部内部状态后才提交目标 terminal。
`task-terminate --outcome waived` 只有在该 task 的所有 open findings 都有
当前 revision 的有效 waiver 时可达；`accepted` 仅表示承认问题，不能代替 fix/waiver。Supersede 必须
给出已创建且可验证的 successor，不能声称跨 chain 同事务创建。`accept`/`escalate` 必须引用由 `follow-up-create` 预先写入
maintenance chain 的 request/owner assignment 或已存在 successor；CLI 不尝试跨 chain 原子创建。
Waive 必须提供 expiry/next-review；false-positive 必须提供
next-review（可无 expiry）。`record-applied` 同样不负责应用 patch；它只在工作区实际 bytes 与预先
accepted 的 current 原子 candidate generation 完全一致时记录 application revision，否则产生 scope drift。
`audit verify` 是唯一可在全部 completion gates 通过后提交 `campaign-completed-verified` 的命令；
terminal campaign 不可 reopen，后续工作必须新建并显式链接 successor。

所有以 `--work-unit` 为例的命令都以不可复用 instance ID 路由。可保留 `--task <task-id>` 作为 current
generation 中唯一匹配时的便利别名；出现历史/current 多实例、split/merge 后歧义或非 current task 时
必须拒绝并打印可选 instance IDs，不能默认选择“最新”。

授权对象中的 `campaign_max_calls` 是跨所有 run/resume/`--force`/retry 累计的外部调用硬上限；
cache hit 不计外部调用。`--run-max-calls` 只是本次 CLI 的更小安全阀，不能提高授权上限。有效额度为
`min(run_remaining, campaign_authorized_remaining)`；resume 必须从 event chain 重算 campaign 已用量，
不能因新 run 清零。为兼容旧 CLI 如保留 `--max-calls`，只能作为 `--run-max-calls` 的弃用别名。

## 18. 分阶段实施

### Phase 0：防止继续浪费

- 审核范围改为必须显式选择。
- 测试 artifact root 改为临时目录。
- 先实现最小 append-only maintenance event sink，Phase 2 再扩展为 campaign event source 和
  SQLite 投影；Phase 0 sink 已必须使用第 8.1 节 pending-write + fsync + no-replace install，且只允许
  单 writer，在 fencing 实现前拒绝并发写入。
- 按第 8.3 节 schema 记录 elapsed、attempt、token/usage、timeout、cache decision、`run_id` 和可空
  `campaign_id`；非 campaign 事件写入 maintenance chain。
- 统一默认 1,200 秒 timeout；偏离值和 `--force` cache bypass 必须有审计事件。
- 修正 `strict` 的真实语义，同时覆盖 finding validation 与 candidate validation。
- 记录 token estimate-vs-actual；forecast 只用于规划，hard 准入只使用 certified bound，不足时显式
  返回 `budget-admission-blocked`。
- Review index ID 排除时间戳和绝对路径。
- Phase 0 不暴露 `audit plan/run/validate/verify` 半成品命令；继续使用现有单 bundle 入口并接入上述
  instrumentation。campaign CLI 只有在 Phase 2 状态、授权、恢复和 completion 契约同时可用后启用。

### Phase 1：内容寻址与契约适配

- 引入对象库、统一 canonical hash framing、未脱敏 canonical revision、payload digest、result cache key、
  cache observation/conflict、transport config key 和全局唯一 attempt ID。
- 实现 fd-based `SafePublicFileResolver`，所有 bundle/evidence/candidate/test 公开输入共用且 no-follow。
- 使用短 alias，由本地注入 envelope。
- 拆分 local audit envelope 与 model semantic payload，允许安全的跨 campaign 语义缓存复用。
- 实现 evidence 契约与确定性 finding key。
- 定义并 fixture 验证 `codex-review-reply-v2`、`tome4-review-round-v2` 和 Pi disposition payload；
  round context 必须进入 bundle/cache identity，runner 继续强制 `--no-session`/`--no-tools`。
- 定义 verdict reducer、actionable、规范 ledger slice、strict quarantine（`unstable-v1:` 只作隔离区
  identity）和受控类似模式证据请求。
- 对精确输入复用 validated result。
- Cache lookup 在外部授权前运行；实现 empty-plan/cache-only 明确完成路径，冲突 key 禁止自动 attach。
- 细化 redaction 类型，并为 candidate 保留本地 typed span/taint 判定能力。

### Phase 2：Campaign 与增量 planner

- 本阶段实现完成后通过其 phase-owned exit tests；下方编号目录同时含 Phase 1–4 测试，不再把尚未
  实现的后续能力错误设为 Phase 2 入场条件。
- 引入 append-only event source、跨进程 lock、transaction-scoped 短 writer lease/fencing、attempt lease
  和可重建 SQLite 投影；所有 genesis/domain/maintenance/GC progress event 统一使用 crash-atomic installer。
- 实现 per-result-key authoritative classification generation、singleflight、cache-key lock 与
  `classified-pending-target` 恢复 saga；cache attach/resolve/completion 使用同一 generation CAS。
- 实现 campaign/global provider-slot admission saga，并在 `attempt-started` 同一 campaign transaction
  检查 authoritative active count；证明两个 provider 调用可达到 2、第三个被阻断，高风险 cap=1。
- 分离 item identity、revision 与依赖摘要。
- 按 token 和风险生成任务，但采用内容定义式稳定 packing：未触及 hard token/risk limit 时不重包未变化
  work-unit，并优先把变化项隔离。Planner 激活任何 split/merge 前必须展示由重包新增的 cache miss/call；
  无可证明 context closure 的 item-level certificate 时，不得声称不同 bundle 的 cached clean 结论可组合。
- 加入精确授权、scope drift、预算、覆盖率、recover 和 resume。
- 实现初始 authorization/完整 reauthorization 单链、campaign/task lifecycle 控制命令、logical scope
  generation、预创建 terminal follow-up responsibility 与 continuity/independent-final 分离计数。
- 将 plan/attempt 预算分层、cache-first admission、cost mode、attempt reservation/settlement、
  `external-transfer-started`、timeout+grace、round/attempt cancellation 和 remaining budget reducer
  纳入 event source；SQLite 删除或任一事务点崩溃后不得改变任何预算/round 维度。
- 加入宿主分配的稳定 `finding_ref`、round event、`audit respond`、`audit plan-round` 和
  `review-reply` stage；实现 reply replace/freeze、stance/item-revision gate 和新 finding 同 task
  归属，同 task 轮次串行且默认上限为 3。
- 实现 frozen request 下的串行 transport attempts、单一 validated result、payload-repair successor
  request、attempt terminal+result acceptance composite、整轮 disposition 原子 event、evidence
  accept/prepare-round 和 termination 笛卡尔归约/draining。
- 实现 work-unit instance lineage DAG、conserved entitlement reducer、跨 item finding 唯一 owner/
  aggregate task、bounded host revision与一次性 exact host composite 授权模式，以及 `audit drive` 本地编排。

以下是跨阶段契约测试目录。全部使用 fixture provider、临时 artifact root 和公开合成输入，不得
触发真实外发或读取受保护输入；每项的 phase owner 见本节末的退出矩阵：

1. `public_path_allowlist`、item、task 和 `plan_content_key` 无论枚举/并发顺序如何变化都稳定；相同
   purpose/parent/request-event/generation 的 campaign ID 稳定，而相同内容的新 request/generation 得到不同 ID；
2. 规范排序的 candidate groups 可从 base 精确重放；accepted event 中乱序、重复、缺项或额外 group
   被拒绝；已有 accepted chain 时人工复现相同 canonical bytes 通过内容判据，任何 byte-different
   “等价”改写或额外 hunk 在 `exact-candidate-only` 下均为 drift；在明确授权的 bounded mode 下只可
   经 `bounded-host-revision-accepted`、finding binding 和全部累计 cap 进入新 generation；exact 模式
   只有一次性完整 reauthorization+plan acceptance composite 可接入该精确 snapshot；
3. format-on-save、formatter 或 lint autofix 改变 candidate expected canonical 内容时脱离 candidate
   派生，在没有 bounded 或一次性 exact host acceptance 时判定 drift；只读 lint 不改变 revision；
4. 路径 header、上下文或改动行含 redacted literal 的候选降级为 `parameterized-advice`，永不进入
   派生链；
5. 未脱敏 canonicalization 与 redaction payload 碰撞时，task/bundle/result cache key 仍不同；
6. finding 标题改写和跨 item evidence 顺序变化不改 key；任一 evidence 的 item revision、member
   anchor、规范 claim/rule 或 evidence 集变化都会改变 key；
7. writer 崩溃/暂停后由新 writer 取得更大 fencing token，复活旧 writer 的提交被拒绝；writer lease
   在 provider 启动前释放且恢复等待不超过短 TTL，两个 task 的 provider fixture 能真实重叠运行；
8. 仅凭 `campaign-created` 与后续 event 可重建 campaign/SQLite；event 断号、parent 不匹配、
   payload 篡改或 fencing 倒退均失败关闭，`recover` 不猜测补链；
9. `attempt-started` 原子保存完整 lease、`timeout + completion grace` 下界、逐维预算 reservation 和
   snapshot digest；运行中删除 SQLite 并重建后，remaining budget 与 active reservation 完全一致，
   正确 token 的 completion 可按 actual 结算，错误/过期 token、并发重复 lease 和晚到 completion
   不能覆盖结果或释放预算；只有 event chain 中不存在 `external-transfer-started` 且已提交绑定
   terminal 的 pre-transfer failed/expired/cancel composite 可返还，transfer/unknown 均保守扣减；expiry 后响应只产生
   幂等 late-response/非负 settlement adjustment，不能产生第二 terminal 或进入 cache；post-terminal
   hard-bound 违约只产生 state-neutral/maintenance integrity incident，不重写 review state；task/campaign
   终止请求在 active attempt/round/reservation 全部 drain 前不能进入外层 terminal，逐点 crash 可恢复；
10. 获授权派生删除会创建 deletion-verification successor；split/merge/delete predecessor 只有在
    successor 覆盖/finding disposition 全部成功后进入 `task-verified-via-successors`。无 accepted
    candidate/bounded/exact host event 的人工删除或 task 无故消失触发 drift，不能通过 completion gate；
11. finding strict 与 candidate strict 分别失败关闭；有效 finding 不因无效/参数化 candidate 丢失；
    payload repair 只有显式授权且预算充足时执行一次，并累计 call/token/cost；
12. Phase 0 非 campaign usage 写入 maintenance chain；resume/`--force`/retry 不能靠新 run 重置
    campaign call/hard-token 预算，任一 hard 维度耗尽都会显式阻断，forecast 偏差只记录；
13. 跨文件 candidate group 的每个单文件 member 均绑定自己的 base file revision；全组原子成功或
    失败，base/expected mode/type、link count 也必须匹配；重复路径、重叠 hunk、越界/evidence-only
    path 和单 member 失败都不能部分应用；
14. 跨 campaign cache hit 允许 source/target 的 local bundle digest、campaign ID 和 `R-NNN` 不同，
    但 outbound semantic payload、resolved deployment/lineage 和 result key 必须相同；target 用自己的 alias map
    重新验证/物化，并通过 plan count、白名单、kind、revision 与 local cache policy，不能继承 source
    外发授权。命中在 external authorization/attempt admission 前，尚无 authorization 或
    `calls_remaining=0` 仍不产生 attempt/lease/reservation；相同语义的 cache miss 则停在授权/预算 gate。
15. Codex reply 引用未知/重复/已关闭 finding、漏答 open finding、绑定旧 review/revision 或引用
    bundle 外 anchor 时失败关闭；`fixed`/`partially_fixed` 未绑定实际 changed item revision、只改变
    dependency/evidence，或 partial 缺少 remaining issue 时同样拒绝。冻结前 replace 必须 generation
    连续并绑定 superseded digest，append/矛盾 stance 和并发双 replace 被拒绝；冻结后只有完整
    pre-transfer cancel + 显式 reopen event 可在 successor 替换，external transfer 后永不允许；合法
    reply 不直接关闭 finding。
16. Round bundle 的 prior review/reply/规范语义 slice 任一判断字段变化都会改变
    `semantic_round_context_digest` 和 cache key；只改变 campaign/ref、时间戳、CAS 路径、approver、
    usage 或 lease 只改变 local envelope，不改变 result identity；slice 顺序变化经 canonical sort 后稳定。
17. 每个 prior open finding alias 必须恰有一个合法 disposition；未知 alias、越界 evidence、缺失 reason、
    把 new finding 伪装成旧 disposition 或带错误 reviewed revision 时整轮拒绝。组合矩阵至少覆盖：
    `resolved-only → approved`、`still_open → changes_required`、`actionable-new → changes_required`、
    `note-only-new → approved`、`note + context_request → changes_required`、
    `still_open + disputed → disputed`、`insufficient_evidence + context_request → disputed`；模型 payload
    不要求 verdict，adapter 唯一计算并注入。Legacy 顶层 verdict 即使错误也只记录 ignored field，不
    触发 paid repair；其他未知字段仍 strict 拒绝。Validated response 只用一个
    `review-round-validated` event 原子提交整张 map；在任一 finding 前后注入 crash 都只能得到零项或全项。
18. `review-round-planned` 后 instance 的 reply/bundle 冻结；同一 request 的 transport attempt 严格
    串行且只能接受一个 validated result，未走完整 pre-transfer cancel/reopen 的 replace、旧
    revision、重复或晚到结果成为 rejected/stale，不能改变
    ledger。无 attempt 的 round cancel、active reservation 未 transfer 的 attempt+round composite、
    已 terminal pre-transfer attempt set 的 round cancel 和 transfer 后 abandon 都保持 round/预算不变量；
    构造半次 composite 或错误释放
    被拒绝。测试 runner 参数不得出现 `--session`、`-c`、RPC 或文件工具。
19. 连续复核达到默认三轮时按第 9.5 节唯一表归约；未解决项和末轮首次出现的
    blocker/major/minor/note/context request 均进入 `awaiting-terminal-disposition`，禁止第四轮但允许
    terminal 前显式 false-positive/waive/escalate。Action 后 task 唯一进入 success 或 escalated，不能
    永久 pending、自动 waiver、terminal 后补写 disposition，或把同 lineage continuity 计作独立终审。
20. Invalid evidence 输出只进入 `quarantined-unstable`：同一 attempt/raw payload 的 quarantine key 重放
    稳定、跨 attempt 不合并，整个 strict round 失败，且无 finding ref/verdict/waiver/continuation/
    verified 路径；人工 import 必须补齐稳定绑定。`similar-public-pattern-occurrences` 只接受
    rule/alias/anchor，在 allowlist、20 match/5 file 上限内工作，regex/glob、越界或受保护输入被拒绝。
21. Token calibration 按 `(provider, resolved_deployment_id, model_lineage_id, bundle_kind, stage, version)`
    分桶，初审与
    后续 round 不混样；p90 只影响 packing/forecast。Hard reservation 使用 tokenizer/provider contract
    的 certified bound，测试应证明 p90 再保守也不能替代该证明。
22. Calls 及 hard token/cost 只按 attempt reducer 计数，retry/`--force` 各算 attempt，cache hit 不算；
    token/cost 的 hard、forecast、disabled 三态严格区分；hard 缺 certified
    token bound 或 price/currency/snapshot/worst-case reservation 时外发前失败，forecast 超预测只记
    variance。Terminal 原子携带 reservation、usage、settlement/raw-usage digest；SQLite 删除和各
    崩溃点重放不出现双重/遗漏 debit。
23. `maintenance-created` 能在空 artifact root 原子 bootstrap；随后 `campaign-requested` 可触发一个
    无先验 campaign token/event 的 `campaign-created` genesis。Campaign-level event 固定
    `work_unit_instance_id=null, task_id=null`；并发创建只产生一个 genesis，下一 writer 从 token 2 开始。
24. `SafePublicFileResolver` 对每个 path component 做 no-follow 检查；指向受保护 root、仓库外或普通
    allowlist 文件的 symlink/junction/reparse、Git mode 120000、mount/submodule、FIFO/device/socket
    以及多链接 regular file 全部失败。验证与读取使用同一 fd，交换目标的 TOCTOU 测试也失败关闭。
25. Pre-transfer cancelled round instance 不消耗 logical ordinal，同 ordinal generation+1 可规划；transfer
    后 transport failure/timeout 在同一 frozen request 内串行 retry，不创建下一 ordinal。Request/repair
    cap 耗尽则 task failed/follow-up，不能借新 ordinal 重试；只有被 ledger 接受的 validated semantic
    judgment 消耗 continuity ordinal。
26. Reauthorization 只能引用 current parent 和完整 snapshot；绝对累计 ceiling 不因 resume/new revision
    清零，不能低于 finalized debit + active reservations，扩 scope/model/stage/mode 均留下明确 diff/authority。
27. 同一 `plan_content_key` 的 initial-change-review、periodic-review 和 follow-up 由不同
    purpose/request-event/generation
    创建可并存 campaign，并正确链接 parent/successor，不发生 deterministic ID 冲突。
28. Continuity ordinal、request repair、transport attempts 和 independent final review generation 分别
    归约；耗尽三轮 continuity 不隐式增加终审，独立终审也不被误计为“第四轮”。Final instance 具备
    plan/run/validated/pass/escalate 全路径，普通 cache hit 不满足 fresh gate，崩溃重放同 attempt 不外发。
29. 从 planned 到 completed-verified 及每个非成功 terminal 的 CLI/event 路径均可达；缺 reason、
    authority、finding refs、revision 或 successor 的 waive/escalate/cancel/supersede 被拒绝，terminal
    campaign 不能 reopen。Active attempt 下 terminate 只进入 draining；attempt/round/settlement/cache
    flight/provider slot 全部完成后才能 outer terminal，所有 crash 点可恢复且无永久 reservation。
30. GC execute 持有 exclusive CAS barrier 时 campaign/cache/candidate 引用提交阻塞；GC maintenance
    event 走 exclusive-holder direct commit，不递归申请 shared lock。在 dry-run 与 execute 之间新增引用
    会令 manifest 在移动前整体停止；每个 rename/progress event 前后注入 crash 均能幂等 resume/rollback，
    未完成 transaction 阻止新 reference，且不会移动 live object 或死锁。
31. 两个 model alias 解析到同一 lineage 时不满足独立终审；不同且可验证 lineage 才默认满足。Mapping
    漂移、provider serving identity 不匹配和未知 lineage 均失败/降级，不能靠 alias 字符串绕过。
32. 两个跨 item finding 只因 primary alias 不同仍得到同一 key；每条 evidence 均能回映自己的 item/
    revision/anchor，任一绑定变化会产生 continuation 所需的新 key。Task split 时 finding 保持唯一 owner
    或进入一个 aggregate task；重复 owner、部分 evidence ownership 和跨 task 半次 disposition 均拒绝。
33. 所有 ID/hash 使用 domain-separated type/length framing；构造字段边界歧义、不同类型同文本、顺序
    扰动和跨 object domain 碰撞样例时均不会得到错误的相同 identity。
34. 授权 logical scope 内的 candidate/evidence/host-revision/dependency 派生只有对应 accepted event 后才进入新
    generation；每 generation 的 current bundle cap 独立重算，campaign unique outbound semantic
    payload cap 累计不重置，retry/cache hit 不重复计数。Task split/merge 必须携带 generation-increasing
    work-unit instance lineage、finding owner、debit 和 conserved entitlement allocation；新 item/path/kind、
    回边、额度复制或无 lineage/accepted chain 的 revision/evidence 一律 scope drift。
35. 从初审 candidate 到 verified 的端到端 CLI fixture 必须经过 validate、整代 accept、真实 bytes
    record-applied、current-revision reply 和复审；缺 `candidate-accept`、reply 先于 apply、只接受部分
    group 或 record arbitrary group 均失败。无 candidate reply 分支仍可达。
36. 同一 result cache key 的 forced exact duplicate 只增加 observation；per-key generation reducer 在
    target acceptance 前令非等价 validated output conflicted，阻断旧/新 observation 自动 attach/verified。
    Independent resolution 或显式 authority
    可关闭当前 observation set，新增第三种结果会重新打开冲突。
37. Evidence request 可经 attach/accept 进入新 generation；`prepare-round` 对 evidence、reply 和 round
    freeze 全成或全败。拒绝/越界/重复 evidence 有确定 terminal，删除 SQLite 后不出现 accepted evidence
    但旧 plan revision 的半状态。
38. `attempt_id` 在相同 cache key/timeout/ordinal 的不同 campaign、并发 worker 和 `--force` 中仍唯一；
    同一 frozen request 的 transport attempts 串行且最多一个 validated result，payload repair 使用
    successor request 而不改变 continuity。
39. 尚无 external authorization 的 cache hit 可完成，cache miss 精确暂停在 authorization gate；零 task
    只有在成功 plan 与 empty-purpose policy 下完成，提取失败/过滤异常不能伪装 empty-plan。
40. `exact-candidate-only` 不自动接受 byte-different host fix，但允许用户对一个精确 snapshot 通过
    `exact-host-revision-authorized-and-accepted` 一次性继续；`bounded-same-logical-scope` 只有初始确认
    明确展示并且 finding/path/item/bytes/files/hunks/generation/cumulative cap 全满足时接受。新 path/
    kind、secret/redaction 失败或提额必须走明确 scope authority，受保护输入始终不可授权。
41. 单 task 效率 fixture 分别证明 clean=1 次语义调用、普通 fix=2、纯 evidence/defense=2、答辩后修订或要求
    final 的路径通常不超过 3；报告将 `charged_or_possible_transfers`、`provider_request_confirmed` 和
    `validated_results` 分列，且 authorization 预览展示最短/预计/最坏可达调用数。
42. 对 maintenance/campaign genesis、普通 domain event、cache/provider-slot event 和 GC progress 分别在
    pending create、部分 write、file fsync、no-replace install、directory fsync、projection 前后注入崩溃；
    最终 chain 只能停在旧 head 或出现完整新 event，截断 pending 被精确移入 aborted quarantine、永不占
    最终 sequence且不永久堵链。Final 已安装、
    temp/SQLite 未清理时 recover 幂等完成；冲突 final、无可靠 no-replace 原语或无法唯一归属的 temp
    失败关闭，不能覆盖修补。
43. 两个进程对同一冷 result key 同时 miss 时只有一个取得 singleflight/外发，另一个等待后 attach；
    在 classification、target composite、flight close 每点崩溃均可恢复。强制产生非等价 observation 时，
    conflict generation 必须先于任何 target verified，attach/resolve/completion 全部被同一 key lock/CAS
    串行化；stale classification token 被拒绝。
44. Strict-valid review/final/remediation output 不存在孤立 `attempt-completed`：一个 composite 同时结算
    attempt、接受 request 和应用 ledger/candidate result。对 validator 完成、global classification、
    campaign composite、slot/flight close 各点注入崩溃，只能得到唯一 acceptance、明确 conflict/
    unattached outcome或未提交状态，不能出现 terminal attempt + 永久 open request。
45. 穷举 `termination requested × no/possible/confirmed transfer × no/active/failed/expired/validated-pending/
    accepted attempt × planned/pending/terminal request`；每格都按第 8.1 节唯一归约到 cancel、abandon、
    accepted-before-termination 或 outer terminal。特别覆盖 pre-transfer active lease expiry、post-transfer
    failed worker、classification pending 和 termination/result sequence 竞争，drain barrier 最终必空。
46. 两个 campaign 的 base plan instance 不同但 path/item base revision/action/patch bytes 相同，必须得到
    相同 `semantic_candidate_effect_digest` 并归入同一 decision class；target attach 重新物化自己的
    candidate instance/group 并保留 source author provenance。任一 semantic member field 改变则不等价。
47. 默认 exact mode 的无 candidate host fix 可通过一个
    `exact-host-revision-authorized-and-accepted` event 同时重述完整 authorization并接入精确 plan chain，
    无 prior authorization 的 cache-origin campaign 也可在同 event 创建首次完整 authorization；随后
    reply/re-review 可达。任一半 event、未来 byte 变化、新 scope、缺 finding binding 或缺 final
    entitlement 均拒绝。普通 `reauthorize` 单独出现不能让 host bytes 获得 plan acceptance。
48. `{x,y} → {x}+{y} → {x,y}` 的 split/merge fixture 即使复现相同 task/task revision，也生成三个不同
    work-unit instances；edge 只从 `g` 到 `g+1`，SQLite/CLI/finding owner 不混淆历史/current instance，
    构造回边或同代重复实例时失败关闭。
49. Split 前 lineage 已用 2/3 continuity 且只余一个 final/remediation slot 时，successors 共享或显式
    分配 remaining entitlement，不能各自再得到一份；merge 对共同祖先 pool 去重。Generation 改变后
    重新计算 `J/F/max_reachable_calls`，不足时在激活前等待完整 reauthorization，而非运行中途撞 ceiling。
50. 两个 CLI/两个 campaign 并发竞争 provider pool：低风险恰可重叠 2 个，第三个在
    `attempt-started` 前阻断；translation/high-risk 恰可 1 个。分别在 slot pending、campaign attempt、
    slot activated/terminal/release 后崩溃，pending slot 可恢复且从不超发或永久泄漏。
51. Remediation 从 trigger→plan→cache/miss→authorization/attempt→strict result→candidate/advice/no-change
    →candidate accept/apply/review 的每条分支可达；budget/entitlement/cache conflict 和 author influence
    均进入 campaign。直接低层 `tools/pi-remediate` artifact、未绑定 finding/revision 或自报 resolved
    不能进入 canonical ledger/candidate chain。
52. 末轮 `accept`/`escalate` 只有在预先 commit 的 follow-up request、successor campaign 或 manual owner
    assignment 与 source finding/revision 精确匹配时可提交；在 precreate 与 dispose 之间崩溃只留下可用
    responsibility，不会留下无 owner 的 accepted finding。多 finding 最终 composite 只产生 success 或
    escalated terminal，缺绑定、跨链“假原子”或 terminal 后补 owner 均拒绝。

### Phase 3：修订与验证闭环

- Reviewer 支持可选 candidate。
- 翻译候选接入 proposal strict validation。
- 代码候选接入单文件 member、跨文件原子 group 和临时 patch/test 验证。
- 实现 `candidate-accept` 与 `validated → accepted → applied → current reply → re-review` 可达主路径。
- 实现第 13.3 节 remediation planned/request/attempt/cache/result/candidate/CLI 闭环；低层
  `tools/pi-remediate` 结果不能旁路进入 canonical campaign。
- 将 exact candidate 与 `parameterized-advice` 分流，禁止参数化建议或 formatter 输出进入派生链。
- 应用后只重审受影响 task，引入高风险独立复审 gate，并阻止未闭环 campaign 完成。
- 实现 fresh-only independent-final instance/planner/reducer/CLI；transport retry 与 payload repair 不增加
  final generation。
- 接入 Codex reply → Pi disposition → ledger transition 闭环；`resolved` 只有在当前 revision、本地
  validation 和适用独立 gate 全部通过后才能推进为 `verified`。

### Phase 4：受控并发与维护

- 在 Phase 2 已正确执行的 authoritative cap 上增加公平排队、provider backoff 与吞吐调优；安全上限
  仍为公开低风险代码 2、翻译/高风险 1，不能等到本阶段才具备跨进程 gate。
- 低风险任务分层模型/抽样。
- 按 provider/model/bundle kind/stage 校准 token estimator，并审计 estimate-vs-actual、bucket 与
  fallback level。
- Finding waiver 过期、false-positive 抽样和策略提升。
- 带不可变 manifest、CAS shared/exclusive reference barrier、exclusive-holder direct maintenance commit、
  per-object progress、崩溃 resume/rollback、隔离区和完整事件审计的 Artifact GC。

阶段退出测试按能力 owner 划分，编号来自上方目录：

| 阶段 | 必须通过后才能退出的测试 | 不属于该阶段的依赖 |
|---|---|---|
| Phase 0 | 12 的 maintenance/run 记录场景、21 的采样记录场景、22 的 mode schema 场景、41 的指标 schema、42 的单 writer maintenance sink 子集 | 不要求 campaign reducer 或真实 provider |
| Phase 1 | 1、5、6、11 的 finding gate、14/16 的纯语义 key fixture、17、20、24、32、33、36 的 observation reducer、46 的 semantic digest schema | 不要求 event concurrency、candidate application 或 GC |
| Phase 2 | 7–9、12 的 campaign 场景、14–19、21–29、31 的 identity/resolution 场景、34、37–45、47–50、52 的 campaign/transport/authorization/recovery 场景、41 的 drive/preview、42 的全 event-store 场景 | 19/28/31/44/47 中的高风险独立终审或实际修订 gate 与 35/46 target materialization/51 由 Phase 3 完成 |
| Phase 3 | 2–4、10、11 的 candidate gate、13、35、46 的 target candidate materialization、51，以及 19/28/31/44/47 的独立终审/应用/remediation 场景 | 不要求自动 GC 或并发吞吐优化 |
| Phase 4 | 30，并重跑所有早期安全回归与受控并发/限流测试 | 无 |

每阶段只以自己拥有的场景作为 exit gate，不以前一阶段尚未实现的后续能力作为 entry gate；但任何
后续阶段都必须重跑并保持所有已退出阶段的安全回归。Campaign CLI 发布要求 Phase 0–2 全部 owner
场景通过，candidate application 要求再通过 Phase 3，GC execute 只有 Phase 4 场景通过后才可启用。

## 19. 验收标准与效率指标

### 19.1 正确性与边界

- 同一内容在不同文件枚举、SQLite 返回和并发完成顺序下得到同一 `plan_content_key`/task/semantic
  payload identity；campaign ID 还必须对 purpose/parent/request-event/generation 稳定，新的周期触发不能撞回
  已完成 campaign。
- 无关 manifest 变化不使代码 bundle 或其他组件 bundle 失效。
- 未授权 task 无法调用外部 provider。
- candidate group/member digest 与规范排序可确定重放；accepted list 非规范、断代、重复或缺项时
  失败关闭。授权复用只比较预先记录 accepted chain 的 expected/actual canonical bytes：人工复现
  完全相同 bytes 可通过；byte-different 等价改写或额外 formatter hunk 在 exact mode 触发 drift，
  exact 模式可由一次性完整 reauthorization+plan acceptance composite 接入一个精确 snapshot，bounded
  mode 则必须先有完整 `bounded-host-revision-accepted`；新增 logical file/item/kind 不能被普通 host
  acceptance 静默吞入。
- 跨文件 group 的每个单文件 member 都绑定独立 base file revision，并且只能全组原子验证/应用；
  base/expected mode/type/link count 必须匹配，同 generation 重复路径、重叠 hunk 或部分成功均被拒绝。
- candidate 的 header、上下文或改动行只要依赖 redacted span，就只能成为
  `parameterized-advice`；主代理据此修改后必须新 plan，并按 revision mode 取得
  `bounded-host-revision-accepted` 或 `exact-host-revision-authorized-and-accepted`。
- candidate 应用前后禁止 formatter 和修改型 hook；只读 validator 不改 revision，任何 canonical
  内容变化在尚无对应 accepted generation/host event 时均判定 drift。
- Candidate 闭环必须实际经过 validated、整代 accepted、applied、current-revision reply 和 re-review；
  缺少 candidate-accept 的 `record-applied` 不可达。无 candidate 的反驳/人工修订各有独立可达分支。
- `revision_hash` 由未脱敏 canonical 内容计算；构造 redaction 文本碰撞时仍得到不同 task/bundle
  和 result cache key。
- Bundle、补充证据和候选修订均不含受保护路径、授权范围外的仓库内容或凭据。
- 所有公开文件访问经过同一 fd-based no-follow resolver；中间/最终 symlink、junction、reparse、
  Git 120000、mount/submodule、多链接/特殊文件和 TOCTOU 替换均在读取目标前失败关闭。
- Pi 无工具、无隐式 session、无共享工作区写权限。
- 多轮连续性只由 validated review、Codex reply、当前 bounded bundle 和 event chain 重建；删除任何
  Pi 本地 session 都不影响恢复，规范 runner 不接受 `sessionFile`、session ID、`-c` 或 RPC 状态。
- Codex 对每个 open finding 都有唯一、绑定当前 revision 的结构化答复；Pi 对每个 prior finding
  short alias 都有唯一 disposition，未知 alias、漏项、重复项和越界 evidence 不能进入 ledger；本地
  adapter 才把 alias 映射到 `finding_ref`。
- Reply 只在 `review-round-planned` 前按连续 generation replace，旧 digest 由 supersession event
  保留；冻结后不能重写同一 round。`fixed`/`partially_fixed` 必须绑定实际变化的相关 item revision，
  仅 dependency/evidence 变化不能冒充修复。
- Verdict 由宿主按 `disputed > changes_required > approved` 重算；混合状态、actionable new finding、
  note-only、note+context-request 与 insufficient evidence 的组合结果唯一；任何 context request 至少
  为 changes-required，模型不能用自报 verdict 覆盖。
- 整轮 disposition/new finding/context request 只由一个 `review-round-validated` composite 提交；外部
  结果还在同一 event 中 terminalize attempt/settle usage/accept request。任意 crash 点都只能重放为
  全轮或零项，不存在孤立 completed attempt 或 per-finding 半提交。
- Evidence 必须经过 request-bound validate/accept 与新 plan generation；`prepare-round` 对 evidence、
  reply 和 round freeze 全成或全败，没有悬空 accepted evidence。
- `finding_ref` 由宿主稳定分配且不复用；跨 revision 延续生成新 finding key 并显式链接，不能依赖
  标题相似度合并，也不能让 Pi 自报编号覆盖宿主映射。
- 跨 item finding 在 split/merge 后仍只有一个 owner work-unit instance；aggregate task 覆盖完整 evidence set，
  不能复制 finding、部分迁移证据或分 task 处置半边。
- Task/task revision 可以在后续 generation 重现，但 `work_unit_instance_id` 不复用，lineage edge 只从
  `g` 指向 `g+1`。Continuity/final/remediation/repair/force entitlement 在 split/merge 中守恒；任何
  扩容都在 successor 激活前重算最坏调用并取得完整 reauthorization。
- 当前 bundle 的新 finding 在非末轮默认归入同一 task 下一轮并共享轮次上限；末轮 new/unresolved
  finding 无论 actionable/note 都进入 `awaiting-terminal-disposition`，禁止第四轮，并且只在 task
  terminal 前接受明确 local action。Bundle 外问题进入 context request/scope drift，不能自动创建 task
  或重置三轮预算。
- `unstable-v1:` 只标识 quarantine object，不是 finding；出现它时 strict round 失败且不产生
  verdict/ref/disposition/coverage。类似模式证据请求受 allowlist、typed query 和 match/file 上限约束。
- Pi 的 `resolved` 不自动等于 `verified`；三轮上限按唯一表进入 terminal disposition gate，不会由
  reducer 任意选择 disputed/escalated、自动 waiver、静默关闭或无限调用。
- 任一 applied finding 都存在本地验证和受影响 task 的最终复审记录。
- major/blocker/security 候选没有符合独立性要求的复审记录时不能 verified；降级同模型复审必须
  有用户授权和 `degraded-independence` 标记。
- 独立终审有独立 instance/planner/events/CLI/reducer，默认只允许一个 fresh semantic generation；
  普通 cache hit 不满足 gate，同 attempt 的 crash replay 不重复外发，任何非 resolved/new finding
  进入 terminal disposition/follow-up。
- Execution fingerprint 不同只证明 attempt/round 不同，不能单独证明 reviewer 独立；最终 gate
  必须另行验证 provider-qualified immutable deployment、canonical underlying model lineage、候选作者
  和显式降级授权；两个 alias
  指向同一 lineage 时不独立，unknown/drifted serving identity 默认失败关闭。
- Campaign remediation 有独立 planned request、semantic payload/cache identity、attempt/result
  composite、candidate/advice/no-change 输出和 CLI；低层 artifact 不能旁路授权、预算、finding binding
  或 independent-final influence。
- 删除 `state.sqlite3` 后可从 event chain 重建相同状态；event 先完整写入 `.pending`、fsync，再以
  no-replace 原子安装并 fsync 目录。在 pending create/write/install 与 projection 任一点崩溃都只得到
  旧 head 或完整新 event，不会出现截断最终文件、丢失已提交事件或接受 orphan/stale 结果。
- 删除 `campaign.json` 后能由 `campaign-created` 重建全部初始身份输入；运行中删除 SQLite 后，
  `attempt-started` 中正确 lease token 的 completion 仍能验证，逐维 reservation、settlement 和
  remaining budget 与删除前一致。
- 空 artifact root 先由 `maintenance-created` bootstrap，再以 `campaign-requested` 触发无先验 campaign
  token/event 的 `campaign-created` token 1；所有 campaign-level event 的
  `work_unit_instance_id=null, task_id=null`，并发 genesis
  与后续 token 2 可确定重放。
- Logical scope、per-generation current bundle 和 cumulative unique outbound payload 分别 gate；
  candidate/evidence/host revision 派生需要 accepted event，retry/cache hit 不重复计 unique payload。
  Calls 及启用的 hard token/cost 由 attempt reducer gate；semantic cache hit 先于 external authorization/
  admission，尚无授权或零 calls 下也不创建 reservation，source/target local bundle/ref 不同仍需 target
  独立复验。所有 miss/force/classification/attach/resolve/completion 由 per-key singleflight、lock 和
  classification generation 串行化；conflicted/stale-generation key 不能自动 attach。
- Token/cost 的 `hard|forecast|disabled` 明确区分；p90 只用于 forecast/packing。Hard 缺 certified
  tokenizer/output bound 或冻结 quote/price/currency/worst-case reservation 时不能外发；forecast 偏差
  不称授权越界，hard actual 超证明上界则终止为 `budget-integrity-failure`。
- Attempt lease 覆盖完整 timeout 与版本化 completion grace；expired/unknown transfer 保守扣减，只有
  chain 证明从未 transfer 的 failed/expired/cancel composite 能释放 reservation。
- `external-transfer-started` 是 pre/post-transfer 分界；termination 的 attempt/transfer/request 笛卡尔表
  对 pre-transfer cancel、post-transfer abandon、validated-pending precedence 给出唯一转换。任一崩溃点
  恢复都不会遗留 active reservation/slot/round、复活 cancelled round 或双重结算；lease-expired 后的响应只写
  non-terminal late-response 和单调非负 settlement adjustment。
- `external-transfer-started` 只计 `charged_or_possible_transfers`；可信 provider receipt、validated result
  分别统计，报告不能把可能外发写成 provider 已确认请求。
- 新 writer 取得更大 fencing token 后，暂停/崩溃后复活的旧 writer 不能提交事件；campaign 与全局
  provider/risk slot admission 都从 event chain 计算 active lease。默认 concurrency=2 的低风险 provider
  执行可重叠但第三个跨 CLI/campaign attempt 被阻断；high-risk/translation cap=1。Writer lease 在 provider
  启动前释放，writer crash 恢复延迟受短 TTL 约束。
- finding 标题、primary alias 和跨 item evidence 排序变化不改变 key；每条 evidence 均绑定自己的
  item/revision/anchor，任一 revision、规范 evidence 或 member anchor 变化必须改变 key。
- 获授权派生删除通过 deletion-verification successor 和 `task-verified-via-successors` 关闭 predecessor；
  split/merge 同样要求 generation-increasing instance lineage success。无 accepted candidate/bounded/
  exact host event 的人工删除、scope
  手动缩小或 task 无故消失不能使旧 campaign 完成。
- `strict` 必须分别阻止歧义 finding 进入 ledger、歧义 candidate 进入派生链；有效 finding 不因
  其无效 candidate 被丢弃。
- payload repair 没有显式 stage 授权、次数或任一预算时不能调用；获准调用使用 successor request
  和新 prompt/key 并累计 campaign/run call、token、费用和 timeout，但不增加 continuity ordinal。
- Phase 0 的非 campaign usage 有 `run_id`、`campaign_id=null` 并进入 maintenance chain；hard bound
  阻断有显式 event 和用户可操作原因，forecast estimate 不伪装成授权 ceiling。
- `--run-max-calls` 不能重置或提高 `campaign_max_calls`；resume、retry 和 `--force` 的已计费或可能
  外发 attempt 在 campaign 维度累计。
- Hard logical scope/bundle/call/token/cost 任一维度超限均阻断；forecast 维度只报告，hard actual 超过
  certified bound 立即禁止新 attempt、drain 后终止，且不能事后追加授权洗掉越界。
- 已完成 campaign 的 waiver 到期或 false-positive 抽样创建新 maintenance campaign，不修改旧
  campaign，并以有原因的 `--force` 执行周期复检。
- `audit validate`/`audit verify` 均不调用 provider 或修改受审源文件，只写审计 artifact/event；
  缺少最终复审时 verify 明确返回 `re-review-required`。
- Authorization/reauthorization 是完整、单链、绝对累计 ceiling snapshot；stale parent、局部增量、
  降低到已结算+预留以下或扩 scope/model/stage 而无新 authority 均拒绝。
- `--force` 与任何实际 GC 都有原因、manifest 和事件链记录；GC manifest 永远不包含 lock、SQLite
  控制文件或 active lease 引用。Execute 以 exclusive CAS barrier 重扫，和所有 shared reference
  commit 使用同一锁序；maintenance event 使用 exclusive-holder direct commit，per-object progress 可在
  任意 crash 后 resume/rollback，未完成 transaction 阻止新引用。
- Campaign 有 pending/failed/open finding 时不能 completed-verified；取消、失败、升级和 supersede
  都有可达 CLI/event、明确 authority/reason/successor，且是不可 reopen 的非成功终态。Active work
  必须先 draining；unresolved cache conflict、lineage predecessor 或 terminal disposition 同样阻止完成。
- 末轮 `accept`/`escalate` 在 disposition 前必须引用已 durable 的 follow-up request、successor campaign
  或 manual owner assignment；不存在“先 accepted/terminal、崩溃后再补责任人”的状态。
- 所有 ID/digest 使用 domain-separated type/length canonical framing；字段边界、类型或 object domain
  不会因裸拼接歧义碰撞。

### 19.2 效率

- 迭代修复 campaign 的精确缓存命中率目标不低于 50%。
- 协议/schema/item/path 类外部调用失败率低于 2%。
- 相同 bundle 不再重复写入对象库。
- 普通代码审核不会生成全量翻译 bundle。
- 测试运行不会在真实 `.artifacts/i18n/runs` 留下文件。
- 单 task/single-bundle clean 代码流程目标为 1 次 Pi 调用；发生内容修订时通常为初审 + 应用后复审共 2 次；纯答辩/补证
  通常为 2 次；答辩后再修订或需要独立终审时通常不超过 3 次语义调用。Transport retry/payload
  repair 单列为异常调用，不能把 clean 基线写成“默认两次”。
- 无 candidate host fix 在 bounded 与一次性 exact 两种模式下都保持“初审 + 复审”2 次外部调用；exact
  模式多一次明确 authority pause，但不会为了接入 plan 额外调用模型。触发独立 remediation 时通常为
  初审 + remediation + 最终复审共 3 次。
- 精确 cache-only 流程为 0 次外部调用且不要求外部转移授权；`audit drive` 把 plan/cache/local verify
  合并为一次用户操作，只在 miss、共享工作区应用和 terminal disposition 处暂停。
- 每次授权展示最短/预计/最坏可达 call；默认 hard ceiling 8 只有在所有启用 stage、retry、repair 和 force
  的 worst-case 和不超过 8 时才称为充分，否则必须关闭可选分支或明确 reauthorize。
- 预算报告显式显示 `J`、`F` 及 retry-only `2J+2F`、retry+repair `4J+4F` 上界；lineage generation
  变化后在 successor 激活前重算。Split/merge 不能复制 entitlement，也不能把运行中 admission failure
  当作正常效率策略。
- 同 result key 的并发冷 miss 通过 singleflight 合并为一次外发；等待者随后 cache attach，不各自
  消耗 reservation。Provider 调用仍可在不同 key/task 上达到安全 cap 2。
- 多轮答辩只重发当前 task 的最新有界内容、未关闭 finding 和必要证据，不重发完整 session
  transcript；每轮 round context 可精确缓存，已验证的无关 task 不重新调用。
- 记录每 campaign 的 attempts reserved、charged-or-possible transfer、provider-confirmed request、
  validated result、失败数、缓存命中/冲突、finding/actionable/no-change 比例、
  prompt/completion token、estimate-vs-actual、token 来源、timeout、retry、cache bypass、
  singleflight joins/avoided calls、provider-slot wait/peak/cap blocks、transfer state、预算
  reservation/settlement、校准 bucket/fallback、预算阻断、elapsed、可用时的
  成本和存储增量。

## 20. 待 Pi 对抗性审核的问题

核心契约已在本稿中做出选择；后续 Pi 公开变更审核不再泛问“是否合理”，而应尝试构造反例：

1. `canonical-hash-v1` 的 domain/type/length framing、canonical sort 及各版本字段能否被字段边界、
   类型混淆、跨 object domain 或平台编码差异制造 identity 碰撞。
2. `plan_content_key` 与 campaign purpose/parent/request-event/generation 的拆分能否既复用相同内容，又允许
   周期性/follow-up campaign 并避免 idempotency 重放创建第二实例。
3. `SafePublicFileResolver` 能否在任何读取前拒绝中间/最终 symlink、junction/reparse、mount、Git
   120000/submodule、特殊文件、TOCTOU 替换和指向 protected root 的路径；是否仍有旁路 runner。
4. Maintenance/campaign genesis、nullable campaign-level `task_id`、pending-write/no-replace event
   installer、transaction-scoped 短 writer fencing 和 CAS→event→SQLite 在空目录、并发创建、删库恢复
   和每个 fsync/install 点崩溃下是否只得到旧 head 或完整新 event。
5. 完整 reauthorization 单链、logical scope generation、per-generation bundle cap 与 cumulative unique
   outbound cap 能否被 resume、局部 patch、candidate/evidence/host revision 派生或 scope contraction
   重置/绕过；bounded mode 是否可能吞入未绑定修订。
6. Hard token/cost 的 certified bound 与 forecast p90 是否完全分离；provider actual、usage 缺失、
   late settlement 或价格漂移能否造成未授权 debit、负调整或事后洗白。
7. Local audit envelope 与 model semantic payload 的拆分能否安全跨 campaign 命中；per-key singleflight/
   classification generation 是否令 miss、force、attach、resolve、completion 真正串行化；非等价
   observation 是否在 target acceptance 前必然冲突。
8. Attempt lease expiry 后的 late response、attempt-terminal+result composite、termination 笛卡尔表、
   pre/post-transfer cancel/abandon、同 request 串行 retry 和 payload repair 能否在所有 crash/sequence
   下保持一个 accepted result、单调 settlement、空 drain barrier 和有限 continuity。
9. Codex reply 的 replace/freeze/reopen、evidence accept/prepare-round、整轮 disposition 原子 event 和
   宿主 verdict reducer 能否抵抗漏项、半提交、旧 revision、错误 legacy verdict 或并发 replace。
10. Strict quarantine 是否保证 invalid evidence 令整轮失败且永不产生 ref/verdict/coverage；payload
    repair 和人工 import 是否是唯一受预算/授权约束的恢复路径。
11. 跨 item finding 的每条 evidence 是否都绑定自己的 item/revision/anchor；task split/merge/delete
    是否使用 generation-increasing work-unit instance DAG，并保证唯一 owner、lineage success terminal、
    deletion verification 与 conserved entitlement，而不重复/丢失 finding 或调用名额。
12. Continuity ordinal、request repair、transport attempt 与 independent-final generation 是否完全分离；
    末轮 terminal-disposition 表和 fresh-only final state machine 是否唯一、可达且不能得到“第四轮”。
13. Model alias mapping、resolved immutable deployment/lineage 和 serving identity 能否防止两个同 lineage alias
    伪装独立 reviewer；unknown lineage 的降级是否只能由显式用户授权进入。
14. Candidate group 的 campaign-neutral semantic effect 与 target-local instance identity 是否正确拆分；
    validate→整代 accept→apply→current reply→re-review、bounded/exact host fix 和 remediation candidate
    是否都可达，且不能被乱序、重叠 hunk、参数化建议或 source campaign provenance 绕过。
15. Finding/task/campaign 的 accept/waive/escalate/cancel/supersede/complete CLI 是否全部可达、可审计；
    accept/escalate 是否只能绑定预创建 follow-up responsibility；termination draining 是否保证 outer
    terminal 前所有 attempt/reservation/round/cache-flight/provider-slot 已结算。
16. GC shared/exclusive barrier、exclusive-holder direct maintenance commit、progress journal 和 incomplete
    transaction gate 能否同时消除锁升级死锁、scan/commit race 与 partial-move 崩溃。
17. Phase-owned exit matrix 是否允许先交付 Phase 0/1，又不会提前开启依赖 Phase 2/3/4 的 campaign、
    candidate application 或 GC execute 命令。
18. 全流程 fixture 是否持续证明 Pi 无工具、无 session、无工作区写权限，且任何 protected DLC
    路径/内容都不能经 bundle、evidence、candidate、cache、raw output 或诊断 artifact 外泄。
19. Empty-plan/cache-only campaign 是否为 0 次调用；单 task 的 clean/fix/evidence/high-risk 最短路径
    是否分别为 1/2/2/2–3 次调用；多 task campaign 是否按 cache-miss task 求和；报告
    是否把 possible transfer、provider-confirmed request 和 validated result 分开，而非用一个布尔数冒充。
20. 两个独立 CLI/campaign 是否既能在不同 key 上达到低风险并发 2，又绝不突破 campaign/provider/risk
    cap；provider-slot pending/activate/release 的每个 crash 点是否可恢复且不超发。
21. `J/F`、retry/repair 和 remediation/final entitlement 是否在每次 lineage generation 后重算；默认
    ceiling 8 是否只在具体 frozen graph 证明可达时展示为充分。
22. Default exact 模式下 byte-different host fix 是否只能由一个完整
    `exact-host-revision-authorized-and-accepted` composite 接入，而普通 reauthorization 不会留下“可外发
    但 plan 不接受”或反向半状态。
23. Campaign remediation 与 terminal follow-up 是否各自有独立 request、authority、cache/state/result/
    responsibility 路径；直接低层 artifact 或跨 chain 假原子是否始终不能进入 canonical completion。
