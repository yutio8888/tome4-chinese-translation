# Paseo 轻量编排 v2 设计

> 状态：设计草案，运行时解耦版。
>
> 契约版本：`paseo-orchestration/2.17-draft`（取代 `paseo-orchestration/2.16-draft`；更早的
> `paseo-orchestration/2.15-draft` 已归档）。
>
> 上位规则：[`AGENTS.md`](../AGENTS.md)。本文约束角色行为、任务边界和候选一致性，
> 不固定具体运行时载体；创建参数按当前 Paseo 接口和本地可用配置提供。

本文面向个人翻译项目。目标是用 Paseo 获得“一个 agent 实现、另一个 agent 复审”的
收益，同时保持失败后容易人工接管，不把短期运行时选择写成长期行为契约。

---

## 一、设计取舍

### 保留的约束

1. 同一 workspace 同时只有一个任务内容写入 agent；ORCHESTRATOR 可写编排记录和验证产物。
2. 主代理定义范围、独立验证并裁决 finding。
3. EXECUTOR、REVIEWER、SENIOR_REVIEWER 和 SCOUT 都使用当前 workspace；只读角色不得修改
   任务内容。
4. 自动修复最多五轮；第二轮后的普通 review finding 必须先经 SENIOR_REVIEWER 按个人项目
   尺度校准，才能触发后续 FIX。
5. 任务开始前记录工作树，结束前运行适用门禁。
6. Paseo 激活期间角色路由独占，不并行使用已归档项目 Skill 或其独立 agent。
7. 四类子 agent 必须由当前 ORCHESTRATOR 通过 Paseo 管理接口创建，并建立可验证的父级
   lineage；不得用其他编排通道替代。
8. 角色由 `labels.role` 绑定，REVIEWER 的具体行为由 `labels.purpose` 绑定。运行时
   载体、版本、档位和回退选择不是本契约的验收条件。
9. 修改翻译流程或项目基础设施时，REVIEWER 和 SENIOR_REVIEWER 必须独立交叉审核每个
   code review phase，再由 ORCHESTRATOR 对照裁决。
10. 每个 code review phase 冻结 SPEC、SPEC 范围内的任务变更路径集、可复现的 diff 生成
    配方和一份包含任务新建 untracked 文件的有界任务自身 diff，用最小 `candidate_ref`
    绑定实际审核候选。
11. 只有实际 diff 重构了可能阻塞测试进程的扫描／解析循环时，才增加短超时微型探针；
    挂起／OOM 后禁止无界重跑，无法经一次有界诊断归因时交给用户。
12. 每个任务在 STATE 记录任务级 `orchestration_transport`，只允许 `cli|mcp`；
    两种传输必须保持相同的 role、purpose、workspace、lineage、恢复和只读语义。
13. 每次 child 调度前，ORCHESTRATOR 必须读取实时 `list_profiles`，根据 profile notes
    与当前 provider/model 能力选择；provider、model、mode、thinking 和 fallback tuple
    只属于运行时选择，禁止进入 STATE schema、candidate identity 或 review contract identity。
    provider、model、mode、thinking 和 fallback tuple 不写入 STATE、candidate identity 或
    review contract identity。
14. 可用性按 provider 处理：同一 provider 的另一个 profile 只能是复杂度升级，不能在该 provider 已不可用时充当 availability fallback。reviewer 尽量避开候选作者的 provider；候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核，但必须仍满足角色、
    purpose 与候选边界。
Before selecting any reviewer profile, ORCHESTRATOR must freeze the implementation candidate, re-enumerate the task's allowed changed paths, and persist candidate_author_agent_id in the task-scoped `.ai/task/<task_id>/STATE.json` at that freeze/path-re-enumeration event.
The persisted candidate_author_agent_id must point to the latest accepted output that was produced or materially changed by the current task's lineage-verified EXECUTOR, not to an author inferred from another task's STATE.
When the candidate changes, ORCHESTRATOR must recompute candidate_author_agent_id before the new review dispatch; it is immutable within a freeze, and ORCHESTRATOR must not traverse another task's STATE to invent it.
candidate_author_agent_id is null for review-only work and for an implement candidate that predates any managed EXECUTOR.
15. 实现候选在冻结及路径重枚举时、选择任何 reviewer profile 前，把当前任务作用域
    `.ai/task/<task_id>/STATE.json` 的 `candidate_author_agent_id` 写成当前任务中、经
    lineage 核验的 EXECUTOR 的稳定直接 `agent_id` 指针；它指向最近一次由该 EXECUTOR
    产出或实质改变冻结候选的已接受输出。候选改变时必须在新的冻结事件重新计算；冻结期间该
    指针不可改写。review-only、或早于任何受管 EXECUTOR 的实现候选，其指针为 `null`。
    ORCHESTRATOR 不得遍历其他任务的 STATE 臆造作者。
16. 每个候选绑定的 REVIEWER 或 SENIOR_REVIEWER dispatch 都复制同一
    `candidate_author_agent_id`；该副本在 dispatch 内不可改写，且不得进入 `candidate_ref`、
    `candidate_identity`、review JSON 或 review-contract identity。只有对应 reviewer 条目
    的 `child_dispatches` 记录 `author_provider_resolution=verified|unavailable|not_applicable`；
    review JSON 不记录该枚举。The immutable per-dispatch author pointer is copied to every candidate-bound reviewer dispatch and cannot be rewritten within that dispatch; it is excluded from candidate_ref, candidate_identity, review JSON, and review-contract identity. `not_applicable` 统一表示 review-only、早于受管 EXECUTOR 的
    实现候选，或没有冻结代码候选的 `scope_audit`。
17. 每次 reviewer dispatch（含恢复）前，先按 `candidate_author_agent_id` 查询 Paseo
    实时元数据，包含已归档 agent；在读取 transport 的显式 provider 前，必须核验 agent id、
    workspace、task／role label、parent lineage 和 EXECUTOR role。基础设施查询只重试一次；
    缺失或表示不同的 provider 字段即为 `unavailable`，不得用 memory、profile 名称、title
    或 provider heuristic 推断。作者记录缺失，或 agent id、workspace、task／role label、
    parent lineage、EXECUTOR role 任一身份核验失败，均在一次重试后将
    `author_provider_resolution` 记为 `unavailable`；显式 provider 缺失或表示不同也同样记为
    `unavailable`。Only the corresponding reviewer entry in STATE child_dispatches records author_provider_resolution=verified|unavailable|not_applicable; review JSON excludes this enum, which is recorded only after unambiguous child creation or adoption and re-resolved before using a recovered reviewer dispatch. Before consuming the transport's explicit provider, ORCHESTRATOR must query live Paseo metadata including archived agents and verify the author agent id, workspace, task/role labels, parent lineage, and EXECUTOR role. If the author record is missing, any of the author agent id, workspace, task/role labels, parent lineage, or EXECUTOR role checks fails, or the explicit provider is missing or differently represented, retry the lookup once, then record author_provider_resolution=unavailable without inferring a provider. `verified` 只表示 lookup 与身份核验成功，不表示选到了不同
    provider。已验证时优先避开作者 provider；主要订阅 provider 的同 provider 预算例外只能
    建立在 verified 上。The same-provider budget exception is allowed only when the author-provider resolution is verified; unavailable resolution remains a soft preference failure. `unavailable` 是诚实的软失败：不得宣称例外成立，可以继续选择合格
    dispatch，但作者 provider 避让此时不可执行。
After ambiguous-create reconciliation or recovery, ORCHESTRATOR must re-resolve author_provider_resolution before using the dispatch, and a temporarily missing enum alone must not force WAIT_USER.
not_applicable is used for review-only work, implement candidates predating any managed EXECUTOR, and scope_audit with no frozen code candidate.
18. 配对 code review 的第二个 reviewer 创建时，取得两名 reviewer 的实时精确 model identity
    （第一名即使已归档也要查询），核验不相等后才在两条 reviewer `child_dispatches` 记录上
    写入 `model_diversity_verified=true`。该布尔值与上述枚举都是可更新的 operational field，
    不是 candidate 或 review identity；有效的 true proof 只适用于完整且成对的记录。
At creation of the second reviewer, ORCHESTRATOR must obtain both live exact model identities, verify exact inequality, and only then persist literal `true` for model_diversity_verified on both reviewer dispatch entries.
    When paired reviewer exact model identities collide, archive the second child before creating a fresh retry child, preserving the role, purpose, workspace, lineage, and candidate binding. If either exact model identity remains unavailable after one retry, enter `WAIT_USER` and do not infer identity from provider, profile, title, memory, or enum. If a second reviewer exists or was unambiguously adopted but either `model_diversity_verified` proof is missing or partial, re-resolve both exact model identities once; persist literal `true` on both entries when they differ, archive the second child and fresh-retry on collision, and enter `WAIT_USER` if either identity remains unavailable. fallback 必须创建 fresh child，保持 role、purpose、workspace、
    parent lineage 与 candidate binding 不变，且不得 resume 已完成或已归档 child。
Operational author_provider_resolution and model_diversity_verified fields are excluded from runtime tuples, candidate identity, review-contract identity, review JSON, and offline STATE-checker closure predicates.

### 明确删除的复杂度

本版本不要求：

- 为角色指定固定运行时载体、版本、mode 或 thinking 档位；
- 任务开始前的运行时发现、精确元组预注册／持久化和固定 primary／backup 路由；但允许在
  reviewer 创建或恢复时对保留的实时元数据做一次有界核验、比较精确 model identity，并
  从比较结果持久化上述 operational enum／boolean；这些衍生字段不等于运行时元组；
- `selected`、回退原因与具体运行时选择绑定；
- 因运行时切换而修改 STATE、升级契约版本或重跑行为审核；
- 专用控制器、workspace 锁、operation WAL、通用文件 hash、immutable artifact store、
  父子 hash 链或 outbound payload manifest；
- REVIEWER 输入的固定字节数／文件数上限；
- 常驻 RSS 监控、进程监督器、强制内存沙箱或通用循环静态分析器。

### 非目标

- 不让模型自动裁决 finding 或替代主代理验收。
- 不让 Paseo SENIOR_REVIEWER 承担译文审核。
- 不自动 commit、stage、reset、删除用户改动或重启 Paseo daemon。
- 不迁移或重解释已有 flat `.ai/task/`、`.ai/reviews/` 记录；新任务写入自己的子目录。

---

## 二、角色

| 角色 | `labels.role` | 责任 | 写权限 |
| --- | --- | --- | --- |
| ORCHESTRATOR | `orchestrator` | 范围、委托、验证、裁决、用户沟通 | 编排记录和验证产物；不改任务内容文件 |
| EXECUTOR | `executor` | 实现 SPEC 中的修改并运行 focused tests | SPEC 允许的任务文件；不得改编排记录 |
| REVIEWER | `reviewer` | 独立审查代码、工具、测试、文档或译文语境 | 只读；只返回 findings 或 observations |
| SENIOR_REVIEWER | `senior-reviewer` | 范围校准和高影响流程交叉复审 | 只读；只返回 assessment/findings |
| SCOUT | `scout` | 只读源码侦察，返回压缩代码上下文 | 只读；只返回上下文，不产生 finding |

所有子 agent 都不继承主会话的隐含任务状态。briefing 必须包含当前角色的范围、验收
标准和必要上下文。角色身份由 task／role label、workspace 和 parent lineage 共同确认，
不能只凭标题或会话文本推断。

Paseo 在任务明确采用本流程并建立 task ID 时激活，到 `DONE`／`STOP` 或明确记录回退
时结束。明确回退只允许在尚未创建 child，或所有 `child_dispatches` 都已
`archive_confirmed=true` 时发生；否则先 reconciliation，无法确认则进入 `WAIT_USER`，
不得退出 Paseo 后由主代理继续。已归档 Skill 产生的输出不得当作 Paseo contract 结果。

---

## 三、模式与审核路由

任务模式只有两种：

- `review_only`：只形成并裁决 findings，不自动修复。
- `implement`：实现、验证、独立复审，必要时最多修复五轮。

审核类型可以有一个或多个：

- `code_legacy_v1`：`role=reviewer`、`purpose=normal_review`，接收代码／工具／
  测试／文档 diff。
- `translation_contextual_v1`：`role=reviewer`、`purpose=translation_contextual_v1`，
  接收独立契约规定的有界译文语境 bundle。

`purpose` 是同一 REVIEWER 角色的行为分支，不是运行时选择。两种审核都必须使用当前
workspace、独立的冻结输入和对应输出 schema。

SPEC 还必须声明 `change_class: standard|translation_workflow|infrastructure`。
`translation_workflow` 指提取、合并、lint、review、build、发布、质量评价等翻译流程
或其契约的改动；`infrastructure` 指会改变共享 artifact、身份／指纹、缓存／增量、
CI／门禁、编排或发布链路的改动。后两类的 `code_legacy_v1` 必须由普通和高级
reviewer 从同一输入独立交叉审核。

混合任务可以共用 task ID、SPEC 和 STATE，但必须分别运行各类审核，不能把术语、Facts
或历史 finding 注入译文审核输入；任一 contract 的输出都不得改写另一 contract 的冻结
输入。

源码侦察不是审核类型：SCOUT 输出只作上下文，不进入 `review_contracts`、不计入
pending/completed、不产生 finding，也不参与 `candidate_ref` 冻结。

---

## 四、轻量状态机

### 仅审核

| 当前状态 | 事件 | 后继状态 |
| --- | --- | --- |
| `PLAN` | 审核开始 | `REVIEW` |
| `REVIEW` | 全部 contract 输出返回，且需要的 cross review 已完成 | `ADJUDICATE` |
| `REVIEW` | 候选在 contract 完成前改变 | 丢弃旧输出、重新冻结候选并留在 `REVIEW`；范围需确认则 `WAIT_USER` |
| `ADJUDICATE` | findings 已裁决且无 deferred | `DONE` |
| 任意非终态 | 需要用户决定 | `WAIT_USER` |
| 任意非终态 | 用户取消或无法继续，且全部 child 已确认归档 | `STOP`；否则 `WAIT_USER` |

`review_only` 的 DONE 表示 findings 已冻结，不表示没有 finding。

### 实现任务

| 当前状态 | 事件 | 后继状态 |
| --- | --- | --- |
| `PLAN` | EXECUTOR 已创建 | `IMPLEMENT` |
| `IMPLEMENT` | EXECUTOR 完成 | `VALIDATE` |
| `VALIDATE` | 定向验证通过 | `REVIEW` 或 `RE_REVIEW` |
| `VALIDATE` | 验证失败且仍有剩余轮次 | `FIX` |
| `VALIDATE` | 验证失败且轮次耗尽 | `WAIT_USER` |
| `REVIEW`／`RE_REVIEW`／`FINAL_REVIEW` | contract 和 cross review 完成 | `ADJUDICATE` |
| `REVIEW`／`RE_REVIEW`／`FINAL_REVIEW` | 候选改变 | 回到 `VALIDATE`，范围不明则 `WAIT_USER` |
| `ADJUDICATE` | 存在 deferred finding | `WAIT_USER` |
| `ADJUDICATE` | 有 accepted finding 且需范围校准 | `SENIOR_REVIEW` |
| `SENIOR_REVIEW` | `scope_audit` 返回 | `ADJUDICATE` |
| `ADJUDICATE` | 有 accepted finding 且仍有轮次 | `FIX` |
| `ADJUDICATE` | 无 accepted/deferred finding | `FINAL_REVIEW` |
| `FINAL_REVIEW` | 无 accepted/deferred finding | `FINAL_VALIDATE` |
| `FINAL_VALIDATE` | 所有 AC 与适用门禁通过 | `DONE` |
| `FINAL_VALIDATE` | 失败且仍有剩余轮次 | `FIX` |
| 任意非终态 | 需要用户决定 | `WAIT_USER` |
| 任意非终态 | 用户取消或无法继续，且全部 child 已确认归档 | `STOP`；否则 `WAIT_USER` |

`cycle` 在每轮 FIX 开始时增加，最大值为 5。门禁失败与 reviewer finding 共用这五轮。
当 `cycle >= 2` 时，客观验证失败可直接触发 FIX；普通 review finding 触发的后续 FIX
必须先走当轮 `SENIOR_REVIEW`。旧 scope audit 不得用于新一轮 findings。

进入 `WAIT_USER` 时，STATE 的 `wait` 保存简短 `reason` 和 `resume_state`；验证中的
挂起／OOM 先完成一次有界诊断，仍无法归因才进入 `WAIT_USER`。

---

## 五、任务记录

每个 v2 任务使用独立子目录：

```text
.ai/task/<task_id>/SPEC.md
.ai/task/<task_id>/PLAN.md
.ai/task/<task_id>/BASELINE.patch
.ai/task/<task_id>/baseline/
.ai/task/<task_id>/CODE_DIFF-<phase>-<cycle>-<attempt>.patch
.ai/task/<task_id>/SCOPE.json
.ai/task/<task_id>/CONTEXTUAL-ENVELOPE-<dispatch_id>.json
.ai/task/<task_id>/EVIDENCE-RECONCILIATION.json  # required for schema 3 review_only infrastructure/translation_workflow; may be empty
.ai/task/<task_id>/STATE.json
.ai/reviews/<task_id>/review-NN.json
```

仅在任务需要时创建 BASELINE、baseline、SCOPE 和 contextual envelope。已有 legacy flat 文件保持
原路径和内容；新任务不得复用已有 task ID，也不得覆盖其他任务记录。

### SPEC 与 PLAN

SPEC 必须写明任务模式、范围、允许修改文件、禁止扩展项和可执行验收标准。PLAN 只记录
主要步骤和依赖，不维护逐动作日志。

### 最小 STATE

```json
{
  "schema_version": 3,
  "task_id": "example-001",
  "mode": "implement",
  "change_class": "translation_workflow",
  "review_contracts": ["code_legacy_v1", "translation_contextual_v1"],
  "state": "PLAN",
  "review_phase": null,
  "pending_review_contracts": [],
  "completed_review_contracts": [],
  "cycle": 0,
  "max_cycles": 5,
  "workspace_id": "...",
  "orchestrator_agent_id": "...",
  "orchestration_transport": "cli",
  "baseline": {"patch": null, "copies_dir": null},
  "candidate_author_agent_id": null,
  "executor": {"role": "EXECUTOR", "agent_id": null},
  "reviewer": {"role": "REVIEWER", "purpose": "normal_review", "agent_id": null},
  "contextual_reviewer": {
    "role": "REVIEWER",
    "purpose": "translation_contextual_v1",
    "candidate_identity": null,
    "dispatch_id": null,
    "input_path": null,
    "agent_id": null
  },
  "scout": {"role": "SCOUT", "purpose": "source_scout", "agent_id": null},
  "senior_reviewer": {
    "role": "senior-reviewer",
    "purpose": null,
    "agent_id": null
  },
  "child_dispatches": [],
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": [],
  "senior_review_records": [],
  "wait": null,
  "last_error": null,
  "updated_at": "..."
}
```

已创建 child 的持久化条目使用 canonical role literal，例如
`{"role":"REVIEWER","lifecycle":"archived","archive_confirmed":true}`；运行时
`labels.role` 仍使用小写 `reviewer`。

`contextual_reviewer` 和 `scout` 是条件字段：只有任务实际选择相应角色／purpose 时
才写入。语境派发后，`candidate_identity`、`dispatch_id`、`input_path` 和
`agent_id` 必须非空并与当前冻结候选一致；SCOUT 不产生审核记录。

STATE 在阶段变化、contract 完成、agent ID 变化、出现错误或 child 生命周期字段变化时
更新；每次 `archive_attempts_started` 递增必须在外部归档调用前立即持久化。
`orchestrator_agent_id` 在任务内不得改变。角色字段是当前契约身份；历史运行时元数据
不参与新任务的有效性判断。

`child_dispatches` 是紧凑的 dispatch 历史；每次创建 child 追加一条记录，记录保留至任务
结束且不得删除。每条记录保存 `role`、`purpose`、`agent_id`、`lifecycle`、
`archive_confirmed` 和 `archive_attempts_started`；语境 REVIEWER 的记录还必须保存不可变的
`candidate_identity`、`dispatch_id` 和 `input_path`。child 创建成功后 `agent_id` 必须
非空，且这些身份字段创建后不可修改。新持久化 role 只写 `EXECUTOR`、`REVIEWER`、`SCOUT`、
`senior-reviewer`；`labels.role` 仍使用小写运行时值。`lifecycle`、`archive_confirmed`、
`archive_attempts_started`、`last_error` 和 `archived_at` 是生命周期字段，按传输结果在
保留的原记录上更新。持久化 canonical role 集合为 `EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer`。
`archive_attempts_started` 初始为 0，最大为 2（首次尝试加一次自动
重试）。`lifecycle` 至少区分 `active`、`stopping`、`terminal`、
`archive_pending` 和 `archived`，而 `archive_confirmed` 只有在传输返回可核验的归档状态
后才可为 true。当前 active dispatch 是角色当前字段所指向的、且状态为 `active` 的唯一
记录；只有它可以在恢复时复用。

当前 ORCHESTRATOR 进程必须有非空 `PASEO_AGENT_ID`。每个子 agent 都必须由当前 ORCHESTRATOR 进程直接创建，使用 agent-scoped 的 Paseo 创建
接口或其 CLI 等价操作。创建载荷至少包含 workspace、task／role label 和初始 briefing。
Paseo daemon 必须以 `PASEO_AGENT_ID` 对应的 ORCHESTRATOR 建立 parent lineage，并在状态
面报告 `ParentAgentId` 或等价的 `paseo.parent-agent-id`；不得用 top-level placement 或
其他 agent 创建接口替代。角色和 purpose label 必须与 STATE 一致。

### Review 记录

每份 review 记录必须保存 `task_id`、`review_contract`、`review_phase`、`cycle`、`attempt`、
`reviewer_role`、`purpose`、`dispatch_id`、`agent_id` 和完成状态。新写入的
`review_records`、`senior_review_records` 是 workspace-relative review 文件路径的数组；
reader 兼容旧 mapping。语境 review 还必须保存
`candidate_identity`、`dispatch_id` 和 `input_path`。每份 code review
记录还保存派发时的 `candidate_ref` 和恰含 `spec_path`／`diff_path` 的
`candidate_locator`；candidate_ref 精确为 `SHA256(SPEC 原始字节 + 一个 NUL 字节 +
diff 原始字节)`。派发、返回和 contract 完成前的引用必须一致。

记录只保存 finding、证据、裁决和结果，不要求复制完整 prompt、运行时选择或构造 lineage
manifest。已完成的历史记录不重写。

`EVIDENCE-RECONCILIATION.json` 是 proposer assertion，不是 reviewer finding，也不替代
ORCHESTRATOR 的独立裁决；reviewer 仍须直接核对其中列出的源记录，并检查是否漏列与候选
相关的 review。`scope_audit` 记录若采用新的复合 finding ref，`calibration` 或
`assessments` 的 key 必须为 `<review path> / <finding id>`，且由
`python3 -B tools/review_evidence.py check-audit` 解析到其 `source_reviews`；历史主题键记录
不因本规则被重写。

对于 `schema_version >= 3`、`mode == review_only` 且 `change_class` 为 `infrastructure` 或
`translation_workflow` 的任务，必须在冻结候选中写入并冻结 `EVIDENCE-RECONCILIATION.json`，
即使它是空 map；缺少 bound code-review completion record 或任一 bound code-review diff 未冻结
sidecar 都会使 DONE 失败。其他模式或分类在 sidecar 出现时校验；候选引用审核记录时，任务
也可在自己的目录写入该文件。它必须是
只含 `schema_version`、`task_id`、`source_reviews`、`claims`、`findings` 的 JSON object，且
`schema_version` 为 1。`source_reviews` 是 `.ai/reviews/` 下的 workspace-relative 普通文件
路径数组；每个源记录中的 finding 由 `{review, id}` 复合引用，且每个源 finding 必须恰好有一
个 `included`、`excluded` 或 `duplicate_of` disposition。included 必须列出至少一个已定义
claim；excluded 与 duplicate_of 必须有非空 reason；duplicate_of 必须是指向 included finding
的 `{review, id}` 对象，不能自指或形成链。claim ID 必须唯一且至少被一个 included finding
引用。source_reviews 不得有重复路径。`classification` 是可选自由字符串；不得保存 `counts`，数量由
`python3 -B tools/review_evidence.py render` 从源记录派生。空 source_reviews 只在 claims 和
findings 都为空时允许。checker 不判断 claim 是否被事实支持。

`candidate_author_agent_id` 是冻结时写入任务作用域 `.ai/task/<task_id>/STATE.json` 的
候选作者指针；它与 `child_dispatches` 中的每次 reviewer 副本属于候选绑定元数据，不是
provider、model、mode、thinking 或 fallback tuple。指针在同一冻结候选内不可变，候选改变时
由 ORCHESTRATOR 在下一次冻结事件更新。指针是 immutable candidate field；
`author_provider_resolution` 与 `model_diversity_verified` 只可出现在适用 reviewer 的
`child_dispatches` 条目中，属于可更新的 operational fields，不能写入 review record。
`author_provider_resolution` 只在 child 创建／adoption 已无歧义后记录；ambiguous-create
reconciliation 与 recovery 都要在使用前重新解析，暂时缺 enum 本身不触发 `WAIT_USER`。
`not_applicable` 是统一枚举值，适用于 review-only、早于受管 EXECUTOR 的实现候选，或无冻结
代码候选的 `scope_audit`。

### 离线终态检查与采用边界

`python3 -B tools/ai_state_check.py STATE.json [--target DONE|STOP]` 离线检查持久化
closure：非终态 preflight 必须传 `--target`，终态可由 STATE 自动选择。`DONE` 组合检查
schema、已关闭 review contract、review-record 到 dispatch 的绑定、冻结候选、绑定 dispatch 的
lineage、implement 的最终验证、finding 清空及所有 child 已归档；`STOP` 只要求无 child 或
每个 child 的规范化 lifecycle 为 `archived` 且 `archive_confirmed` 为 literal `true`。
A child counts as archived only when its normalized lifecycle is `archived` and `archive_confirmed` is literal `true`.

对于每个 bound code-review completion record，DONE 还按以下五项检查：

1. 若其冻结 diff 含有严格的新建 `EVIDENCE-RECONCILIATION.json` entry，checker 从唯一 hunk
   的加号行（含 `\\ No newline at end of file`）重构 bytes，并校验 reconciliation；最新
   `(cycle, attempt)` record 的重构 bytes 必须与磁盘 sidecar 字节相等。多次 attempt 各自独立校验。
2. sidecar 存在时，SPEC 或 diff 中精确出现的
   `.ai/reviews/<task>/review-NN.json` 与 `senior-audit-NN.json` 路径都必须在 `source_reviews`；
   通配符和 basename 不会被解析。
3. `schema_version >= 3`、`mode == review_only` 且 `change_class` 为 `infrastructure` 或
   `translation_workflow` 时，每个 bound code-review completion record 的 diff 都必须冻结
   sidecar；否则失败原因为 `evidence_reconciliation_required`。implement 模式只在 sidecar
   出现时校验。
4. `orchestrator_agent_id` 必须与每个 bound completion record 的 `agent_id` 不同；schema
   低于 3 或缺失时，只有该字段存在才比较，schema 3 起要求它是非空字符串。
5. schema 3 起，`senior_review_records` 中 `purpose == scope_audit` 的记录若存在，必须通过
   `check-audit` 的复合引用检查；scope audit 本身不是必需的 contract。

`python3 -B tools/review_evidence.py inventory review.json...` 只生成源记录的原始字段和
finding ID 清单；`check` 返回结构化 reconciliation 结果，`render` 输出表格及派生 cycle
counts。这些命令都不访问 Paseo、Git 或网络。

`.ai/legacy-cohort-manifest.json` 是 B-prime 采用时的 task-id 边界，不是历史审计或快照清单。
它的唯一 schema 是 `{"schema_version": 1, "unsupported_tasks": ["..."]}`，数组按字典序且
无重复。列入的 task 仅返回 `UNSUPPORTED_LEGACY`（信息性 exit 3）；所有未列入 task 必须走完整
新契约，绝不因缺少新字段而转用历史语义。

### 运行时 profile 路由

`list_profiles` 是每次 child 调度前的实时发现入口；profile notes 和当前能力共同决定
选择，文档不预注册具体 provider/model 组合。provider 可用性不能由同 provider 的升级
profile 伪造；fallback 只能是保持全部编排身份与候选绑定的 fresh child。候选作者与
reviewer 的 provider 避让及仅在 `author_provider_resolution=verified` 时可用的主要订阅 provider 预算例外不改变只读、purpose 或候选边界。
交叉审核必须使用不同的精确 model identity；不同 provider 优先；强制交叉审核无法组成不同
model 时进入 `WAIT_USER`。

作者 provider 的恢复必须查询包含 archived agent 的实时 Paseo metadata，并在消费显式
provider 前核验 `candidate_author_agent_id`、workspace、task／role label、parent lineage
和 EXECUTOR role；一次基础设施重试后仍缺 provider 或身份表示不一致即记录
`author_provider_resolution=unavailable`。它是软偏好不可执行的诚实标记，不能据此使用主要
订阅 provider 例外；若核验成功才记录 `verified` 并优先避让。review-only、早于受管
EXECUTOR 的实现候选以及无冻结代码候选的 `scope_audit` 均记录
`author_provider_resolution=not_applicable`。恢复时重新解析并更新该枚举；暂时缺失枚举不单独
触发 `WAIT_USER`。

第二个配对 reviewer 创建时必须实时取得两名 reviewer 的精确 model identity（第一名可已
archived），核验不相等后在两条 reviewer `child_dispatches` 记录持久化
`model_diversity_verified=true`。恢复时只有完整且成对的 literal true 才是 proof；若第二个
reviewer 已创建或被无歧义采用而 proof 缺失或部分存在，必须按第 18 条的 recovery clause 一次
重新解析两者。上述 live 比较和 derived operational provenance 不改变离线 STATE checker 的
closure predicates。

---

## 六、Paseo CLI 与 MCP 等价语义

CLI 和 MCP 是等价传输，不改变角色、purpose、workspace、lineage、label 恢复、只读和
候选一致性要求。本文只规定编排语义；运行时选择参数按当前 Paseo 接口和本地环境提供，
不进入 STATE 规范、不作为验收条件。

| 目的 | CLI／Paseo | MCP 等价操作 |
| --- | --- | --- |
| 创建 workspace | `paseo workspace create` | `create_workspace` |
| 列出 workspace | `paseo workspace ls` | `list_workspaces` |
| 创建 child | `paseo run` | `create_agent` |
| 状态／lineage 核验 | `paseo inspect` | `get_agent_status` |
| 按 label 查询 | `paseo ls --label` | `list_agents` 后宿主侧过滤 |
| 活动／等待 | `paseo logs`、`paseo wait` | `get_agent_activity` |
| 发送 briefing | `paseo send` | `send_agent_prompt` |
| 取消／归档 | `paseo stop`、`paseo archive` | `cancel_agent`、`archive_agent` |

任务开始时记录实际使用的 `orchestration_transport`。恢复分为三个有序路径，不得用同一
过滤配方混合处理：

1. **创建结果不明确**：此时本地可能还没有 `agent_id` 或 active 历史。直接从传输状态面
   按 workspace／cwd、`labels.task_id`、`labels.role`、需要的 `labels.purpose`、parent
   lineage，以及语境的 `candidate_identity`／`dispatch_id` 过滤；过滤先于基数判定：
   先排除已经存在于 `child_dispatches` 的历史 ID，但不得按远端 lifecycle 排除尚未
   记录的结果。无匹配可重试创建一次；唯一匹配且身份全部正确时，无论其状态如何，先把
   完整不可变身份、观测到的 lifecycle 和初始生命周期字段追加到 `child_dispatches`。lifecycle 为
   active 才更新当前 role 字段并复用；archived 必须先核验归档状态，再记为
   `archive_confirmed=true`，且不得重试创建；terminal／stopping／archive_pending 记录则按
   已保存的 `agent_id` 进入生命周期 reconciliation，不得复用。多个匹配、列表截断或
   身份无法确认时进入 `WAIT_USER`。不得
   因为本地尚无 active 记录就把远端唯一候选
   当作零匹配，也不得盲目创建第二个写入 agent。
2. **重启后的生命周期 reconciliation**：先按 `child_dispatches` 中的已知 `agent_id`
   逐条核对所有 `archive_confirmed=false` 的记录。已到终态者先收获／判废输出，再按
   `archive_attempts_started` 的剩余预算归档；`stopping` 者先确认终态再归档；
   `archive_pending` 者按第七节只读核验。完成这些处理前
   不进入 active 会话恢复，也不创建 successor。
3. **当前 active dispatch 恢复**：生命周期 reconciliation 完成后，只按当前 role 字段
   指向的唯一 `active` 记录及其 `agent_id` 恢复，并重新核验 role、purpose、workspace、
   lineage 和候选绑定。`stopping`、`terminal`、`archive_pending`、已确认 `archived` 的
   历史以及其他旧 dispatch 全部排除；即使 Paseo 列表仍显示它们，也不得制造多个匹配或
   被恢复。

所有需要基数判断的查询都遵守过滤先于基数判定；截断或不完整列表不得当作零匹配。

创建或恢复后必须核验：

1. agent 属于当前 workspace；
2. `labels.task_id`、`labels.role` 和需要的 `labels.purpose` 精确匹配；
3. parent lineage 精确等于 `orchestrator_agent_id`；
4. REVIEWER／SENIOR_REVIEWER／SCOUT 未造成工作树变化；
5. 语境 REVIEWER 的 candidate／dispatch／input 绑定正确。

Paseo 状态面无法暴露可验证 parent lineage 时，停止该 child 并进入 `WAIT_USER`，不把
不可验证状态当作通过。

---

## 七、托管 child 生命周期与即时归档

每次 Paseo-managed child dispatch 都是生命周期意义上的单次运行。该规则适用于
`EXECUTOR`、`REVIEWER`、`SENIOR_REVIEWER` 和 `SCOUT`；一个已完成的 child 不得被当作
可继续交互的长期会话。

child 的运行到达终态后，ORCHESTRATOR 必须先收获其输出并将结果验证为有效或无效，随后
通过当前选定的传输立即归档该 child：CLI 使用 `paseo archive`，MCP 使用
`archive_agent`。归档确认属于 dispatch 完成的一部分；在确认前，不得进行 phase
transition，也不得为该任务创建 successor child。无效输出同样必须先归档，再创建 fresh
retry child。普通 child 保持相同 role、purpose、workspace、parent lineage 和候选绑定；
语境 REVIEWER 保持同一 `candidate_identity` 与冻结 `input_path` 字节，但必须分配新的
`dispatch_id` 和 `agent_id`。

归档保留 task／review 记录中的历史 `agent_id`。已归档 child 不得恢复，也不得发送
follow-up prompt；后续 FIX 或 re-review dispatch 必须创建 fresh child，并重新核验所需的
role、purpose、workspace、lineage 和 candidate binding。

归档失败最多重试一次；首次尝试和一次自动重试合计最多两次。每次调用归档操作前，必须
先持久化递增 `archive_attempts_started`，再调用 CLI／MCP；进程在递增后崩溃或调用结果
不明确时，该次预算保守地视为已消耗，恢复时先只读查询实际归档状态。若未归档且计数为 1，
才允许最后一次自动重试；计数达到 2 后仍无法确认归档状态，必须把记录标为
`archive_pending`、保持 `archive_confirmed=false`，记录 `last_error`，保存
`wait.reason=archive_pending` 与 `resume_state`，并进入 `WAIT_USER`，不得创建 replacement
或推进 phase。恢复 `archive_pending` 时只读核验传输状态：若已归档则补写确认并继续；若
仍未确认，不得再次归档、恢复该 child 或创建 successor。恢复不会重置或增加预算；状态
仍不可确认时继续停留 `WAIT_USER`，直到用户解决外部归档状态并确认归档；在此前不得进入
`STOP`。

用户取消或需要停止仍在运行的 child 时，必须先执行 CLI 的 `paseo stop` 或 MCP 的
`cancel_agent`，然后重新 inspect 并确认其状态已经是终态（包括明确的 cancelled／stopped
终态）；未确认终态不得 harvest、archive、phase transition 或创建 replacement。stop／cancel
请求或终态确认最多各做一次有界重试；重试后仍在运行、状态不可见或状态矛盾时，必须记录
`last_error`，保持 `lifecycle=stopping`，进入 `WAIT_USER`，不把它当作已取消。若传输支持
`force-archive`，也只有该操作自身返回可核验终态时才可使用，不能绕过终态确认。

进入 `DONE` 或 `STOP` 前，ORCHESTRATOR 必须 reconciliation 所有仍被管理的 child，并
归档其中任何尚未归档的 child；只有所有 child 都已得到可核验的归档确认后，才能进入
`DONE` 或 `STOP`。进入 `WAIT_USER` 不得仅因等待用户而取消仍在运行的 child；但已经
到达终态的 child 仍必须归档。CLI 与 MCP 保持完全等价的生命周期语义，
本规则不绑定任何 runtime provider 或 model identity。

---

## 八、角色执行与恢复

EXECUTOR 只修改 SPEC 允许的文件，不 commit、不 stage、不删除或弱化失败测试。完成后
ORCHESTRATOR 检查实际 diff、越权文件和 focused tests。

REVIEWER 按 `purpose` 选择输入和输出契约。普通 REVIEWER 只接收 code／tool／document
diff；语境 REVIEWER 只读取独立契约指定的冻结 envelope 和其引用内容。两者不得互看
另一 contract 的 findings。

SENIOR_REVIEWER 的 `purpose` 只能是 `cross_review` 或 `scope_audit`。当任务修改
翻译流程或基础设施时，它与普通 REVIEWER 从相同 SPEC 和 diff 独立复审；当第二轮后普通
finding 仍要求修复时，它只校准当轮意见，不扩展审核范围。

SCOUT 只返回压缩源码上下文，不进入 review contract、不产生 finding；同一任务同时最多
一个活动 SCOUT。

运行时失败时，按基础设施重试规则处理；如需更换普通 child，必须创建同 role、同 purpose、同 workspace、同 lineage 和同候选绑定的新会话。语境 REVIEWER 更换时保留同一 `candidate_identity` 与冻结 `input_path` 字节，但使用新的 `dispatch_id` 和 `agent_id`。旧未验收输出作废，不得与新输出混合。无需判断失败属于哪一种运行时或为其填写固定回退元组。

---

## 九、Review 输入与输出

普通 code review 只接收有界 baseline→current 任务 diff、SPEC、验收标准和必要上下文。
reviewer 只返回 findings；SENIOR_REVIEWER 只返回 assessment/findings；SCOUT 只返回
上下文。严重度、verdict 和范围建议都不自动生效，由 ORCHESTRATOR 独立核验和裁决。

译文语境审核使用独立的 `translation_contextual_v1` 契约：冻结有序 revision、译文
快照、术语子集、邻近译文、source tags／runtime keys 和固定源码证据；输入不包含先前
finding、裁决或建议修复。

Before freezing or hashing a translation_contextual_v1 payload, ORCHESTRATOR must run the deterministic offline contextual-anchor preflight with the task-scoped `.ai/task/<task_id>/SCOPE.json` and the exact seven-key draft payload.
The preflight also accepts the whole-section form for sections without actual chapter-title t(...) calls.
The task-scoped SCOPE.json must declare only workspace-relative ordinary allowed files plus file, section_path, and ordered actual chapter-title anchors; unsafe, duplicate, missing, or ambiguous declarations fail closed.
An anchor scope may instead declare ordered_titles: [] only when its section contains no actual chapter-title t(...) calls; a titled section with [] fails closed and must declare explicit anchors.
Each declared anchor window begins at its actual chapter-title t(...) call and ends at the earliest later actual chapter title, later section marker, or EOF, so undeclared titles still bound the window.
For ordered_titles: [], the window is the whole section from its section marker to the earliest later section marker or EOF.
ORCHESTRATOR may freeze the payload only after every translation_snapshot source is proven to be the decoded first argument of a real t(...) call inside a declared anchor window; the preflight adds nothing to the payload, candidate_identity, review JSON, or STATE closure identity.
The same source proof applies to a whole-section window, and the preflight adds no payload or identity fields.

当 code review briefing 涉及 evidence-citing candidate 时，ORCHESTRATOR 必须同时交接冻结
候选中引用的 source review paths 和 task-scoped `EVIDENCE-RECONCILIATION.json` 路径；无需交接
inventory 的临时输出，REVIEWER 应直接重新运行 inventory 或读取规范记录。REVIEWER 直接核对
sidecar 的每个复合引用，并把未列出的相关 review、缺失 disposition、错误 duplicate target
或无 reason 作为 finding；这些语义判断不由 checker 代替。

---

## 十、验证与完成

实现前记录：

- `git status --short` 和实际 changed／untracked 文件；
- 任务模式、change class、允许文件、禁止扩展项和 AC；
- 如需接触既有脏文件，保存可恢复的 baseline。

每轮实现后：

- 运行与变更直接相关的 focused tests；
- 涉及译文时运行 `python3 -B tools/i18n lint --strict`；
- 按冻结 SPEC 和任务基线生成任务自身 diff；
- 核对 EXECUTOR 越权文件、REVIEWER／SCOUT 工作树变化和候选引用。

完成前：

- 所有 contract 已完成且 findings 已裁决；
- implement 模式无 open accepted finding；
- 最终 AC 与适用门禁通过；
- 旧用户改动、历史 task 和 archive 未被改写；
- DONE、STOP 或明确回退前，未创建任何 child，或全部 `child_dispatches` 已确认归档。

仅改变运行时选择而未改变 role 行为、输入边界或输出 schema 时，不需要重新解释候选
身份，也不要求为运行时选择变更启动行为复审；修改本契约的角色、权限、候选绑定或
结果 schema 时，仍按 infrastructure 变更审核。

---

## 十一、外发与兼容

外发边界按角色和 purpose 授权：

- EXECUTOR：任务 briefing、SPEC 允许的 workspace 内容；
- 普通 REVIEWER：有界代码／工具／文档 diff、SPEC 和必要上下文；
- SENIOR_REVIEWER：同一 SPEC／diff 及范围校准所需的普通 findings；
- SCOUT：组件范围、公开源码根和机制问题；
- 语境 REVIEWER：冻结的有界译文语境 bundle，以及其中明确引用的译文和公开源码。

所有角色都必须遵守各自的只读、读取范围和输出 schema。改变外发内容范围、目的或
读取边界仍需用户授权；运行时载体不再构成单独的授权轴。

质量 evaluator 的运行身份、预注册、campaign ledger 和历史 assessment 属于独立质量
实验契约，不由本文迁移或重解释。已完成 task、review record、handoff 和 archive 保持
原样；活动旧任务不自动改写，下一次新派发按 role／purpose 记录。

---

## 十二、验收

本文交付至少满足：

1. STATE、创建／恢复、外发和验收只依赖 role、purpose、workspace、lineage、权限和候选
   一致性，不依赖固定运行时身份；
2. EXECUTOR 唯一性、reviewer／SCOUT 只读守卫、candidate_ref 和语境
   candidate_identity 规则仍完整；
3. `translation_contextual_v1` 仍是译文审核唯一活跃路由，结果 schema 和冻结 envelope
   规则不变；
4. CLI／MCP 只作为等价传输，运行时选择不写入 STATE 规范；
5. 历史 task、review artifact、archive 和质量 evaluator 预注册不被重写；
6. 文档之间的 role／purpose／lineage 语义一致，Markdown 和 `git diff --check` 通过。
7. 禁止 runtime tuple 的预注册／持久化，但允许 reviewer 创建／恢复时的有界 live comparison
   以及仅由其产生的 `author_provider_resolution`／`model_diversity_verified` operational
   provenance；该 provenance 不进入 candidate 或 review identity。

---

## 十三、修订记录

| 版本 | 状态 | 内容 |
| --- | --- | --- |
| `2.12-draft` | 设计草案 | 增加完成即归档、保留 dispatch 记录、不可变身份字段、持久化 `archive_attempts_started` 预算与原地更新生命周期字段；明确 `archive_pending` 在外部归档状态解决并确认前必须停留 `WAIT_USER`，拆分创建歧义发现、已知终态 reconciliation 与 active 恢复，明确语境重试保留候选／输入但更换 dispatch／agent，并要求 `DONE`／`STOP` 前完成全部归档。 |
| `2.13-draft` | 上一版草案 | 固定 `lifecycle` 与 canonical persisted role literals，保留 reader alias；记录路径数组、dispatch-to-review 绑定、NUL 分隔的候选身份和离线 `DONE`／`STOP` closure checker 及 B-prime adoption boundary。 |
| `2.14-draft` | 上一版草案 | 增加可恢复的 `candidate_author_agent_id`、归档 metadata 核验和 `author_provider_resolution` 三值枚举；明确 unavailable 的软偏好语义、reviewer child 的 operational field 分类，以及第二 reviewer 创建时的 `model_diversity_verified` 证明、碰撞 fresh retry 和 exact-identity 不可用时的 `WAIT_USER`。 |
| `2.15-draft` | 上一版草案 | 增加冻结／哈希前的离线 contextual-anchor preflight：任务作用域 SCOPE、实际 chapter-title 边界和 source-within-window 证明；它不改变 reviewer 可见的七键 payload 或任何 identity。 |
| `2.16-draft` | 上一版草案 | 增加条件性 EVIDENCE-RECONCILIATION.json、确定性 inventory/render/check/check-audit，以及 DONE 的 sidecar 候选绑定、引用一致性、前瞻性 presence、reviewer/orchestrator 身份不等和 scope-audit 复合引用检查。 |
| `2.17-draft` | 当前草案 | 扩展 contextual-anchor preflight：无实际 chapter-title 的 section 可用 `ordered_titles: []` 声明 whole-section window；含 chapter-title 的 section 对空数组 fail closed，且不改变 payload 或 identity。 |
