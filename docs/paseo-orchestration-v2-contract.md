# Paseo 轻量编排 v2 设计

> 状态：设计草案，运行时解耦版。
>
> 契约版本：`paseo-orchestration/2.25-draft`（取代 `paseo-orchestration/2.24-draft`；更早的
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
3. 普通串行任务的 EXECUTOR、REVIEWER、SENIOR_REVIEWER 和 SCOUT 使用当前 workspace；受管
   wave 则使用下文唯一的跨 workspace 直系 child 拓扑。只读角色不得修改任务内容。
4. 一般任务自动修复最多五轮；schema 4 translation implement 任务默认三轮。4-lane
   译文审核按维护者 standing authorization 使用十轮上限并逐字记录
   `max_cycles_user_authorized=true`；其他情形只有同样记录用户授权才可高于三轮。第二轮后的普通 review finding 必须先经
   SENIOR_REVIEWER 按个人项目尺度校准，才能触发后续 FIX。
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
    只属于运行时选择，不绑定 role／purpose，也禁止进入 candidate identity 或 review contract
    identity。除第 19 条规定的审计性 `runtime_observation` 外，不在 STATE 复制运行时选择。
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
19. 每个新 child dispatch 在身份／lineage 已无歧义且首次取得可核验 live agent metadata 后，
    必须在该 `child_dispatches` 条目写一次 `runtime_observation`。它只原样记录当次 live metadata
    中实际呈现的 provider、model、mode、thinking；缺失字段诚实记 missing，显式 JSON `null`
    必须记为 present/value null。禁止从 profile、title、memory、其他字段或其他 dispatch 推断、
    归一化、复制，也不为历史条目回填。该记录不得参与路由、role／purpose、候选／引用身份、
    review JSON、review-contract identity、完成谓词、wave 判定或 model diversity proof。

### 明确删除的复杂度

本版本不要求：

- 为角色指定固定运行时载体、版本、mode 或 thinking 档位；
- 任务开始前的运行时发现、精确元组预注册／持久化和固定 primary／backup 路由；但允许在
  reviewer 创建或恢复时对保留的实时元数据做一次有界核验、比较精确 model identity，并
  从比较结果持久化上述 operational enum／boolean；这些衍生字段不等于运行时元组；
- `selected`、回退原因与具体运行时选择绑定；
- 因运行时切换而修改 STATE、升级契约版本或重跑行为审核；
- 专用控制器、workspace 锁、全仓通用 operation WAL、文件 hash 或 immutable artifact store（但允许基于目标的 task-bounded journal、hash 与 immutable shadow/snapshot）、
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

### 稳定条款 ID

角色 prompt 只引用下列稳定 ID；完整语义由本文对应章节承载：

| Clause ID | 短触发语 | 规范位置 |
| --- | --- | --- |
| `P2-SINGLE-WRITER` | 唯一任务内容写入者 | 第一、二、八节 |
| `P2-DIRECT-LINEAGE` | 当前 ORCHESTRATOR 直系 child | 第五、六节 |
| `P2-LIVE-ROUTING` | 每次派发前 live profile lookup | 第一、五节“运行时 profile 路由” |
| `P2-RUNTIME-OBSERVATION` | 首次可核验 live metadata 原样留档 | 第一节第 19 条、第五节 |
| `P2-CANDIDATE-FREEZE` | SPEC/diff/envelope 冻结与引用 | 第一、五、九节 |
| `P2-READ-ONLY` | REVIEWER/SENIOR_REVIEWER/SCOUT 只读 | 第二、八、十一节 |
| `P2-REVIEW-INDEPENDENCE` | 配对复审互不读取 findings | 第一、三、八节 |
| `P2-AUTHOR-PROVENANCE` | 作者 provider 只做 live lookup | 第一、五节“运行时 profile 路由” |
| `P2-MODEL-DIVERSITY` | 配对 reviewer 精确 model 不同 | 第一、五节“运行时 profile 路由” |
| `P2-HARVEST-ARCHIVE` | 终态先收获后归档 | 第七节 |
| `P2-FRESH-RETRY` | 无效/替换均 fresh child | 第六至八节 |
| `P2-RECOVERY` | 创建歧义→生命周期→active 恢复 | 第六节 |
| `P2-STOP-CLOSED` | 不可核验即 WAIT_USER | 第四、六、七、十节 |
| `P2-TRANSLATION-CONVERGENCE` | schema 4 译文 full/closure/final-full 收敛 | 第四、九、十节 |

所有子 agent 都不继承主会话的隐含任务状态。briefing 必须包含当前角色的范围、验收
标准和必要上下文。角色身份由 task／role label、workspace 和 parent lineage 共同确认，
不能只凭标题或会话文本推断。

Paseo 在任务明确采用本流程并建立 task ID 时激活，到 `DONE`／`STOP` 或明确记录回退
时结束。连续批次工作（如逐段译文复核）中，一个 task 进入 `DONE` 并提交后可以直接
建立下一个 task ID 并开始，不需要用户逐批确认；每个 task 仍是独立任务，各自完整执行本契约的
冻结、复审、门禁与生命周期要求，不得跨 task 复用候选、review 记录或 child。批次间的连续推进
不改变任何 `WAIT_USER` 条件：本契约要求进入 `WAIT_USER` 的情形仍必须停下并交回用户，不得
因为「保持连续」而绕过。明确回退只允许在尚未创建 child，或所有 `child_dispatches` 都已
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
- `translation_contextual_v2`：仅供 `schema_version >= 5` 的新 task 使用，固定
  `role=reviewer`、`purpose=translation_contextual_v2`；接收独立 v2 契约规定的 full、
  closure 或四成员 compact lane stage。同一 task 不得与 v1 混用。
- `translation_surface_screen_v1`：仅供 `schema_version >= 5` 的新 task 使用，固定
  `role=reviewer`、`purpose=translation_surface_screen_v1`；接收独立
  `docs/paseo-translation-surface-screen-v1-contract.md` 规定的 full 或四成员 q/r lane
  stage，按 `P2-TRANSLATION-SURFACE-V1` 执行 batching 与 carry-over。同一 task 不得与任一
  语境审核契约混用；其结果只是 `OK|ISSUE` observation，不是 adjudicated finding。

`purpose` 是同一 REVIEWER 角色的行为分支，不是运行时选择。各类审核都必须使用当前
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

`cycle` 在每轮 FIX 开始时增加，一般任务最大值为 5。schema 4、`mode=implement` 且包含
`translation_contextual_v1` 的任务默认 `max_cycles=3`，始终要求 `cycle <= max_cycles`；
4-lane 译文审核显式设置 `max_cycles=10` 与 literal `max_cycles_user_authorized=true`；
2–3 lane 保持默认 3。其他上限高于 3 的任务也必须有该 literal。schema 3 及更早任务和
`review_only` 不采用该新机械语义。门禁失败与 reviewer finding 共用对应上限。
这里的旧式 `4-lane/max_cycles=10` 规则与 `translation_contextual_v2` 无关：v2 的四个
contextual lane member 共同组成一个 `(cycle, attempt)` stage，不各自占用 cycle，也不因此
提高默认 `max_cycles=3`。
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
.ai/task/<task_id>/CONTEXTUAL-LANE-GROUP-<group_id>.json  # v2 lane stage only
.ai/task/<task_id>/SURFACE-SCREEN-ENVELOPE-<dispatch_id>.json  # surface screen v1 envelope
.ai/task/<task_id>/SURFACE-SCREEN-GROUP-<group_id>.json  # surface screen v1 lane group only
.ai/task/<task_id>/TRANSLATION-REVIEW-LEDGER.jsonl  # optional append-only review ledger
.ai/task/<task_id>/EVIDENCE-RECONCILIATION.json  # required for schema 3 review_only infrastructure/translation_workflow; may be empty
.ai/task/<task_id>/STATE.json
.ai/reviews/<task_id>/review-NN.json
.ai/reviews/<task_id>/raw-<dispatch_id>.txt               # every accepted v2 record
```

仅在任务需要时创建 BASELINE、baseline、SCOPE 和 contextual envelope。已有 legacy flat 文件保持
原路径和内容；新任务不得复用已有 task ID，也不得覆盖其他任务记录。

### SPEC 与 PLAN

SPEC 必须写明任务模式、范围、允许修改文件、禁止扩展项和可执行验收标准。PLAN 只记录
主要步骤和依赖，不维护逐动作日志。

### 最小 STATE

```json
{
  "schema_version": 4,
  "task_id": "example-001",
  "mode": "implement",
  "change_class": "translation_workflow",
  "review_contracts": ["code_legacy_v1", "translation_contextual_v1"],
  "state": "PLAN",
  "review_phase": null,
  "pending_review_contracts": [],
  "completed_review_contracts": [],
  "cycle": 0,
  "max_cycles": 3,
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
schema-5 v2 禁止 `contextual_reviewer`，改用非空 `contextual_reviewers` 数组。full/closure
当前 stage 恰含一个不带 lane 字段的 pointer；lane 创建时可暂存同组有序前缀 1..k，但派发和
发布时必须恰含四个 pointer，并各自固定 `lane_group_identity` 与 `lane_index`。每个接受的 v2
dispatch 还必须显式保存 `workspace_id == STATE.workspace_id` 和
`parent_agent_id == STATE.orchestrator_agent_id`；字段缺失即失败。

v2 最小替换片段为：

```json
{
  "schema_version": 5,
  "review_contracts": ["translation_contextual_v2"],
  "workspace_id": "...",
  "orchestrator_agent_id": "...",
  "contextual_reviewers": [
    {
      "role": "REVIEWER",
      "purpose": "translation_contextual_v2",
      "candidate_identity": "...",
      "dispatch_id": "...",
      "input_path": "...",
      "agent_id": "..."
    }
  ]
}
```

lane pointer 在这六键上另且仅增加 `lane_group_identity` 与 `lane_index`；v2 STATE 不出现单数
pointer。

STATE 在阶段变化、contract 完成、agent ID 变化、出现错误或 child 生命周期字段变化时
更新；每次 `archive_attempts_started` 递增必须在外部归档调用前立即持久化。
`orchestrator_agent_id` 在任务内不得改变。角色字段是当前契约身份；历史条目缺少
`runtime_observation` 仍然有效，不追溯回填。

`child_dispatches` 是紧凑的 dispatch 历史；每次创建 child 追加一条记录，记录保留至任务
结束且不得删除。每条记录保存 `role`、`purpose`、`agent_id`、`lifecycle`、
`archive_confirmed` 和 `archive_attempts_started`；语境 REVIEWER 的记录还必须保存不可变的
`candidate_identity`、`dispatch_id` 和 `input_path`。child 创建成功后 `agent_id` 必须
非空、不得等于任务的 `orchestrator_agent_id`，且这些身份字段创建后不可修改。新持久化 role 只写 `EXECUTOR`、`REVIEWER`、`SCOUT`、
`senior-reviewer`；`labels.role` 仍使用小写运行时值。`lifecycle`、`archive_confirmed`、
`archive_attempts_started`、`last_error` 和 `archived_at` 是生命周期字段，按传输结果在
保留的原记录上更新。持久化 canonical role 集合为 `EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer`。
`archive_attempts_started` 初始为 0，最大为 2（首次尝试加一次自动
重试）。`lifecycle` 至少区分 `active`、`stopping`、`terminal`、
`archive_pending` 和 `archived`，而 `archive_confirmed` 只有在传输返回可核验的归档状态
后才可为 true。当前 active dispatch 是角色当前字段所指向的、且状态为 `active` 的唯一
记录；只有它可以在恢复时复用。

`runtime_observation` 只允许出现在 `child_dispatches[*]`，且出现时使用 exact schema：

```json
{
  "schema_version": 1,
  "source": "live_agent_metadata",
  "captured_at": "<non-empty timestamp string>",
  "capture_status": "captured",
  "provider": {"presence": "present", "value": "<raw JSON value>"},
  "model": {"presence": "missing"},
  "mode": {"presence": "present", "value": null},
  "thinking": {"presence": "missing"}
}
```

顶层 STATE 与任何 review record 禁止 `runtime_observation`。容器必须恰含上述八个字段：
`schema_version` 是非 boolean 整数 1，`source` 精确为 `live_agent_metadata`，`captured_at` 是
非空字符串，`capture_status` 精确为 `captured`。四个 FieldObservation 中，present 形式必须
恰为 `{"presence":"present","value":<原始 JSON 值>}`，missing 形式必须恰为
`{"presence":"missing"}`；不接受额外键。原始值不做类型收窄、规范化或解释，因此显式 null
与 missing 保持可区分。旧 STATE 可以没有该字段；有效观测不改变 DONE／STOP、wave、candidate
或 review completion 判定。

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
`candidate_identity`、`dispatch_id` 和 `input_path`。schema 4 translation implement 的每份
语境记录还在 envelope 外保存 `review_kind=full|closure`；closure 记录另存
`parent_candidate_identity` 和与子集 keys 同序的 `inclusion`，其 reason 词表固定为
`changed_target`、`open_finding`、`shared_runtime_key`、`narrative_or_term_claim`、
`extra_touched_target`。changed+dependency closure 由 ORCHESTRATOR 根据任务 diff、finding 与
批内依赖确定；现行 v1 不创建 dependency graph、closure manifest 或其他附加 artifact。
checker 只验证记录／envelope 的 cycle、phase、parent、顺序、source 与 inclusion 自洽，不证明
closure 已穷尽依赖；存在歧义时 ORCHESTRATOR 必须派发 `RE_REVIEW/full`。这些字段不进入七键
payload、candidate identity 或结果 schema。每份 code review
记录还保存派发时的 `candidate_ref` 和恰含 `spec_path`／`diff_path` 的
`candidate_locator`；candidate_ref 精确为 `SHA256(SPEC 原始字节 + 一个 NUL 字节 +
diff 原始字节)`。派发、返回和 contract 完成前的引用必须一致。

schema-5 v2 record 使用 `review_kind=full|closure|lane`。每条记录必须保存由 task/dispatch
精确推导的 `raw_output_path` 和 exact returned bytes 的 `raw_output_sha256`；DONE 对记录绑定的
同一 envelope/raw bytes 重跑 strict validator，不允许 fixture、换行或路径特例。lane record
另含 exact seven-key lane object，并与 manifest、dispatch 和创建 labels 四方一致；四条有效
lane record 只能整组发布。closure 使用 `parent_review_kind`／`parent_coverage_identity`，禁止
v1 的 `parent_candidate_identity`。full、closure、lane（包括 FINAL_REVIEW/full）每次派发前都
必须对其实际 identity/path 渲染固定 dispatch prompt，并验证模板与实例均不超过 800 UTF-8
bytes；七键 payload 的 `rendered_briefing` 不受该 prompt byte budget 限制。

记录只保存 finding、证据、裁决和结果，不要求复制完整 prompt、运行时选择或构造 lineage
manifest；review record 明确禁止 `runtime_observation`。已完成的历史记录不重写。

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

### 受管 Phase 1 wave

受管并行 wave 采用且只采用一个跨 workspace 拓扑：`WAVE.json` 中唯一的
`orchestrator_agent_id` 所指 ORCHESTRATOR 通过 agent-scoped 接口直接创建全部 lane 与
integration child。不存在 lane-orchestrator 或中间编排根。每条 lane 使用与
`root_workspace_id` 不同且彼此不同的 workspace；integration 可以使用 root workspace。
每个 task 的 `STATE.orchestrator_agent_id` 必须等于 wave ORCHESTRATOR，且
`STATE.child_dispatches` 只记录该 task 的直系 child。每条 wave child dispatch 必须持久化非空
`workspace_id`、`task_id`、`parent_agent_id` 与 `purpose`：前两者分别等于所属 task 的
`STATE.workspace_id`／`STATE.task_id`，parent 精确等于 WAVE ORCHESTRATOR，purpose 与实际
dispatch 用途一致且非空。`lineage_verified=true` 只是附加声明，不能代替这些原始身份字段。
恢复、归档和歧义 reconciliation 都先
按该 child 的 task workspace 限定，再按 task、role、purpose、parent lineage 和候选绑定过滤，
不得从 root workspace 的列表猜测其他 lane。`ai_state_check.check_wave_state_context` 在普通
`DONE` closure 之外检查这些 wave-only workspace／lineage 条件；普通串行 STATE 不被追溯改写。

角色写权限保持单写入者语义：ORCHESTRATOR 只维护 ignored 的 `.ai/waves/` 编排记录并执行只读
核验；lane EXECUTOR 只写其 lane SPEC 的任务内容；REVIEWER、SENIOR_REVIEWER 与 SCOUT 只读；
fresh integration EXECUTOR 是组合译文的唯一写入者。唯一受跟踪 wave evidence 也只能由同一
integration task 中 lineage 核验的 fresh、归档确认、`purpose=wave_evidence` EXECUTOR 写入；
其 dispatch 必须唯一绑定 `wave_evidence_path` 与 prospective DONE WAVE 的 SHA-256 identity，且
agent ID 不得复用 `integration_apply`／`integration_fix` 或其他 dispatch。必要的 evidence-only EXECUTOR 是该 task
唯一 `task-content-allowed-files/1` 授权面的语义子集，不得另建第二份 allowed-files，也不得改动
任何 `translation_fix_paths` 字节。ORCHESTRATOR 不 cherry-pick、不 apply target、不编辑译文，
也不创建、编辑或覆盖 wave evidence。

Phase 1 的机器入口只能是普通、相对、非 symlink 的
`.ai/waves/<wave-id>/WAVE.json`。`python3 -B tools/wave_review.py` 从该入口绑定并读取
MERGE-QUEUE、CONFLICT-PREFLIGHT、lane-workset、lane／integration STATE、SPEC、SCOPE、
TARGET-PATCH、integration-content-diff、prospective DONE WAVE 与唯一 evidence；CLI 不接受这些
从属路径作为参数。上述 Phase 1 JSON 都使用 exact-key、紧凑 canonical UTF-8 字节；object key
递归排序、array 保持冻结顺序、无额外空白或末尾换行，identity 为这些 canonical bytes 的
SHA-256。路径逃逸、绝对路径、非规范路径、symlink 或 workspace 越界为输入错误。稳定退出码为
`0=PASS`、`1=contract failed`、`2=input/usage error`。

每次调用还必须用重复的 `--workspace-root WORKSPACE_ID=ROOT` 提供 WAVE 当前引用的全部
workspace 的可信 root map。Phase 1 接受 2–4 条 lane（默认 2 条，不允许无界并发）；映射键集合
必须与 WAVE 的 root、全部 lane 和已绑定 integration
workspace ID 精确 1:1；不同 ID 不得解析到同一路径，所有 root 必须是同一 Git common-dir 下的
真实 worktree，且 root workspace 必须就是权威 WAVE 入口所在 worktree。checker 在每个任务所属
root 独立执行 path escape、父目录、symlink、Git object 和 tracked-file 检查；不得从 root
workspace 读取同名的 lane 影子 STATE／SPEC／SCOPE／patch／review／envelope。

`preflight` 必须从 pinned manifest 的唯一 `component.sources.mount`（或该组件的受保护 mount）
定位 `component.translation` 并独立导出 primary，要求其精确等于 workset、lane
`translation_fix_paths` 和 collateral artifact 的声明。Phase 1 lane SPEC 必须含有独占一行的
`phase1_collateral: forbidden`；ordinary 规范常量为 `[]`，授权 remainder 必须重算为 `[]`。
三类集合 identity、调用集合与 workset 的 1:1 关系、pairwise intersections、preflight PASS 和
空 collateral 都从 WAVE 绑定字节重算，不信声明 bool／empty。
`lane-workset/1` 必须非空且 revision、调用定位 1:1；checker 还须使用仓库固定 manifest、LuaJIT
5.1 loader 和 `base_commit^{tree}`／所属 worktree 当前译文逐调用解析完整
`(section, source, source_tag, args_order, special)` 身份。runtime set 精确由 workset 调用重建为
`(source, source_tag)`；Phase 1 dry-run 的 term/narrative provenance 精确由每个
`ordered_revision_keys` 重建为 `narrative_closure` 依赖键。两类声明不得自报为空。

规范门禁命令为：

```bash
python3 -B tools/wave_review.py preflight .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py export-target-patch .ai/waves/<wave-id>/WAVE.json --lane-id <lane-id> <workspace-root-args>
python3 -B tools/wave_review.py verify-target-patch .ai/waves/<wave-id>/WAVE.json --lane-id <lane-id> <workspace-root-args>
python3 -B tools/wave_review.py apply-target-patch .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py verify-content-diff .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py prepare-publication .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py publish .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
python3 -B tools/wave_review.py done .ai/waves/<wave-id>/WAVE.json <workspace-root-args>
```

其中 `<workspace-root-args>` 是对 WAVE 当前全部 workspace ID 各重复一次的
`--workspace-root WORKSPACE_ID=/absolute/git/worktree/root`。

当前 Phase 1 工具的 TARGET-PATCH 能力边界是明确的 no-change dry-run：它严格校验
`target-patch/1`、base commit/tree、final candidate、revision order、workset、queue、额外译文
diff 与当前旧值漂移。空 patch 只有在每个 workset revision 的 candidate target、固定 base
target 和 lane 当前 target 三者逐字节相等时才成立；integration full envelope 还必须按
MERGE-QUEUE 顺序精确覆盖所有 lane workset／最终 envelope 的 key、source、target。遗漏、乱序或
source／target 漂移均失败。工具只导出、verify 和 apply `changes=[]`。任何非空 patch 即使 schema 正确也
fail closed；这不是生产 Lua apply。后续要启用非空 patch，必须另行实现按
`(section, source, source_tag, args_order, special, call_index)` 解析 Lua、重算 base old target、
证明 current old target、拒绝重叠与额外 diff，并经独立契约复审后才能解除此门禁。

no-change closure 还要求每条 lane 及 integration 的全部 `translation_fix_paths` 当前字节逐文件
等于 `base_commit`；这项全文件约束覆盖 workset 外的调用、target 和其他字节漂移，不能由只重算
workset 调用或 whole-file hash 后回填声明绕过。`integration-content-diff/1` 的
`changed_paths` 与 `entries` 必须都严格为 `[]`。`apply-target-patch` 在检查任何 lane patch 前，
必须先读取 integration 的 task-derived STATE／SPEC／SCOPE，核验 task、workspace、共同
orchestrator、唯一 `allowed_files = translation_fix_paths ∪ {wave_evidence_path}`，并找到恰好一个
task／workspace／parent lineage／`purpose=integration_apply` 绑定的 integration EXECUTOR
dispatch；调用进程的非空 `PASEO_AGENT_ID` 必须精确等于该唯一 EXECUTOR 的 `agent_id`，环境变量
缺失、不等、记录缺失或歧义都 fail closed，`integration_fix` 不得代替 apply caller。

每条 lane 的 `fixed_source_identity` 必须从 `base_commit` 固定字节的版本 manifest 重建：公共
Git 组件取其 `source_repository` 的 `commit:<40-lowercase-hex>`，受保护组件取其
`source_baseline.snapshot_sha256` 的 `snapshot:<64-lowercase-hex>`；当前 manifest 字节与
`base_commit` 不同、来源机制缺失、或一个候选跨多个不同固定 identity 都失败关闭。integration
使用全部 lane workset 按 MERGE-QUEUE 顺序重做相同校验，并机械构造其余 provenance：
`bounded_context` 是各 lane 冻结 context array 的顺序串接；`terminology_snapshot` 是下列对象的
canonical compact JSON UTF-8 字节解码字符串：

```json
{"schema_id":"phase1-integration-terminology-snapshot/1","lanes":[{"lane_id":"<queue lane>","terminology_snapshot":"<lane frozen string>"}]}
```

`rendered_briefing` 同样是下列对象的 canonical compact JSON UTF-8 字节解码字符串；数组保持
MERGE-QUEUE／revision 顺序，`translation_snapshot` 的 target 从 integration 当前译文重解析：

```json
{"schema_id":"phase1-integration-contextual-briefing/1","ordered_lane_ids":["<lane>"],"ordered_revision_keys":["<revision>"],"translation_snapshot":[{"revision_key":"<revision>","source":"<source>","target":"<integration target>"}],"fixed_source_identity":"<manifest identity>","terminology_snapshot":"<canonical terminology render>","bounded_context":[{"revision_key":"<revision>","context":"<lane frozen context>"}],"lane_briefings":[{"lane_id":"<lane>","rendered_briefing":"<lane frozen briefing>"}]}
```

仅重算七键 payload／candidate identity 不能替代这些来源校验；空 context／术语／briefing 或任意
重渲染值只要不等于上述机械结果就必须拒绝。

终结恢复只复用冻结字节：GATED 后先用 `prepare-publication` 验证全部 lane／integration
STATE 为真实 `DONE` closure、唯一 final completion record、归档 child、组合 full envelope 和
translation hash，再写 canonical prospective DONE WAVE；由 integration EXECUTOR 写绑定该
identity 的 evidence，随后由 `publish` 在再次核验 evidence／identity／translation bytes 后原子
发布完全相同的权威 WAVE。`done` 只做发布后的 allowed-files／diff／evidence closure。
prospective 已有而 evidence 缺失时续写 evidence；evidence 已有而
权威 WAVE 未发布时，核验引用后发布相同字节；权威 WAVE 已发布时只重跑 closure。任意三者字节
或 identity 不一致都 `WAIT_USER`，不得重渲染或修补哈希。`done` 还重跑 lane／integration STATE
closure、translation-only 内容哈希、唯一 allowed-files 的 base→工作树 diff 与 evidence
publication；成功仅报告外部 `DONE_VERIFIED`，不得把该字段写入 WAVE。
其中每个 lane／integration 的 final full review 必须跨 STATE 的 `review_records` 与
`senior_review_records` 扫描 `REVIEW`／`RE_REVIEW`／`FINAL_REVIEW` 等合法 review phase 的全部
terminal full completion records，并唯一绑定最大 `(cycle, attempt)` 的一条。terminal completion
包含 `CHANGES_REQUIRED`：更新的失败结论必须参与最大值选择并阻断 closure，不能因非 PASS 而先被
过滤。最大 tuple 平局、跨数组重复路径、路径歧义、WAVE 指向较旧 completion 或最新记录不通过
均失败关闭。

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
除审计性 `runtime_observation` 外不进入 STATE，且观测本身不作为验收条件。

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

v2 恢复在上述顺序内额外重验 exact manifest/envelope/raw bytes、raw hash、每个 dispatch 的
workspace/direct parent、创建 labels 和完整 stage。partial lane group 不形成 completion stage；
任一 member 无效或基础设施失败时只保留 child/raw 诊断，归档整组后以更高 attempt 创建 fresh
四成员 group。不得续跑、补写或跨 stage 复用任一 group ID、group identity 或 manifest path。

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

判定挂起或调用 stop／cancel 之前，ORCHESTRATOR 必须先完成一次有界的终态取证，不得只凭
单一 `status` 字段，也不得只凭某字段长时间未更新就断定挂起：

1. 重新查询一次实时状态，并同时读取 `attentionReason`／`attentionTimestamp` 与 activeTurn；
   activeTurn 为空表示没有进行中的运行，此时 child 已结束，不属于挂起。
2. 检查工作树（`git status --short` 与 `git diff --stat`）。未产出任何改动的 EXECUTOR 留下空
   diff；该证据用于区分「结束但未产出」与「运行中卡住」，并确认是否有可收获的成果。
3. 只有在重新查询后仍确认存在进行中的运行且无进展时，才按挂起处理并进入 stop／cancel 流程。

传输状态面的字段可能过期；陈旧字段本身不是挂起证据，也不是取消的理由。取证顺序颠倒或跳过
工作树检查而做出的故障结论无效，必须撤回。

child 结束但输出无效——包括 EXECUTOR 未产出任何改动、未给出报告，或只回了计划／进度说明
——时，按本节的无效输出处理：先归档，再创建 fresh retry child，保持相同 role、purpose、
workspace、parent lineage 与候选绑定。已结束的运行不是可继续的会话：即使 child 仍为 idle 且
尚未归档，也不得对其发送 follow-up 让它续跑，也不得据此跳过归档。

已写入 STATE、`child_dispatches.last_error` 或 review 记录的故障归因被事实推翻时，必须在同一
轮立即更正该记录，写明实际终态与撤回的结论，并向用户说明；不得让已撤回的诊断继续留存。

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


### Bounded EXECUTOR 事务与恢复

1. **目标路径级事务**：禁止 `git reset --hard`、`git checkout` 或任何整树清理。允许非目标路径存在未提交的 dirty changes；对目标路径必须使用 `allowed_paths` 声明的 required preimage state/hash/mode 进行 fail-closed 检查。`allowed_paths` 与恢复 journal 的 `ordered_paths` 使用同一原始 POSIX 路径集合校验，并必须在任何 artifact、journal 或目标写入前拒绝空组件、`.`／`..` 组件、重复或末尾分隔符、任何非唯一规范形式，以及任一路径为另一条路径严格祖先的祖先／后代重叠（与声明顺序无关）；合法兄弟路径不构成重叠。同时拒绝首路径组件为 `.git`、`.ai` 或 `.artifacts` 的 privileged namespace。其他不在该拒绝集中的普通 dot-prefixed 项目文件（例如 `.gitignore`）允许作为目标。拒绝 symlink、目录或特殊文件。状态必须是明确的 `file` 或 `absent`，mode 必须是非 boolean 的整数 `0..0o777`。
2. **Shadow Output 与持久化事务日志**：实现 shadow output 与持久化事务日志，必须写入已忽略的 `.artifacts/paseo-bounded/<workspace_id>/<dispatch_id>/`，不得写入 `.ai/` 或受跟踪目录。artifact helper 与 journal reader 自身必须验证 ASCII identifier allowlist、路径 containment、ordinary-file/no-symlink 和 exact schema，不能信任调用方已完成检查。
   - decoded edit 的 bytes/state/mode 必须与 postimage 完全一致，且所有目标初始状态符合 preimage；任一不一致必须在首个 journal 或目标写入前失败。
   - shadow 与 preimage snapshot 是该事务的 immutable artifact；首次准备及每次中断恢复都必须以声明的 hash/mode 重新验证，验证失败不得触碰目标。
   - artifact 准备开始前先原子持久化 exact-schema preparation identity，绑定 workspace、dispatch、candidate 与 envelope hash。首个 PREPARED journal 尚未持久化时，只能在全部目标仍为 preimage、identity 精确匹配，且现有目录树没有未知文件、symlink 或特殊文件时恢复；已有 artifact 必须逐项通过声明的 hash/mode 复验，缺失的预期 artifact 才可安全补齐。identity 缺失或不匹配、artifact hash/mode 错误、未知条目或目标漂移都 fail closed 且不得触碰目标。
   - file mode `0o000`、`0o200` 等 owner-unreadable 值仍是有效声明。hash 复验不得依赖 root 绕过权限：实现可在保持 file descriptor 打开的有界区间临时增加 owner-read，但必须立即恢复原 mode 后才读取并在返回前复验；`fdopen` 成功后 descriptor ownership 必须立即转交 stream，读取异常不得被重复 close 的 `EBADF` 掩盖；复验完成后的目标以及 immutable artifact mode 必须精确等于声明值，错误时同样 fail closed，不得永久放宽权限。
   - 目标与 journal 使用同目录内不可预测、排他创建且不跟随 symlink 的临时文件，写 bytes、`chmod`、文件 `fsync` 后才 `replace`；replace 或 unlink 后必须 `fsync` 目标父目录。失败时只清理由本事务排他创建且已证明属于该父目录的临时文件，异常不得吞掉。
   - 不得声称多文件 OS 原子，只保证基于日志的可恢复事务。状态机为 PREPARED、APPLYING、COMMITTED、ROLLING_BACK、ROLLED_BACK、ROLLBACK_CONFLICT。APPLYING 恢复时实际 post 但未记入 `applied_paths` 的目标必须补入；ROLLING_BACK 恢复时实际 pre 但仍在列表中的目标必须移除；任何 journal 写入都必须先拒绝未知或重复的 applied path，再将 `applied_paths` 按 `ordered_paths` 唯一重排为 ordered subset；任何既非明确 pre 也非明确 post 的第三种状态必须记录冲突且不得覆盖目标。
3. **拆分 candidate_id 与 envelope_hash**：杜绝循环哈希。新增的这两个标识仅属于 `bounded_apply_v1` envelope/runner，不得替代或全局重构 `translation_contextual_v1` 中已有的 `candidate_identity`。两者必须是 64 字符 lowercase hex。
   - `candidate_id=SHA256(canonical candidate body excluding candidate_id)`，内容绑定 author、allowed_paths、edits、invariants，但不含时间戳与 dispatch 环境。
   - `envelope_hash=SHA256(canonical full envelope excluding envelope_hash)`，绑定 candidate、workspace_id/dispatch_id/parent_lineage/base_revision/preimages/gates/postimages/retry_of。
4. **固定验证顺序与幂等性**：`candidate_id` -> `envelope_hash` -> `workspace`/`lineage`/`base`/`preimages` -> `replay ledger`。
   - 定义 `(workspace_id, dispatch_id)` 幂等：相同 hash 已完成且目标仍匹配 postimage 时返回 `already_committed`，中断按日志恢复；同 dispatch 不同 hash 硬失败。新 dispatch 重用 candidate 必须 `retry_of` 且存在 host 注入、精确绑定 task/workspace/prior dispatch/candidate 的可信 `archive_receipts` 条目，其 `archive_confirmed` 必须为 literal boolean `true`；runner 只验证该事实，不生成或推断 receipt。重试还必须重新冻结 `base`/`preimages`。
5. **规范化 JSON 与 Exact Schema**：
   - Envelope 的 `envelope_version` 必须精确为 `bounded_apply_v1`，journal 的 `schema_version` 必须精确为 `bounded_apply_journal_v1`。Canonical JSON 采用严格无多余空白的 UTF-8 序列化，`allow_nan=False`，字典键按字典序排序；CLI 输入和 journal 都拒绝 duplicate JSON keys。
   - Schema 必须 exact/fail-closed：拒绝额外键、错误类型、重复或缺失 allowed paths、edit/path 不一致、绝对路径、点路径（穿越）、NUL 字符和 symlink。author 必须是精确的 `{role, dispatch_id}` object，其中 `role` 必须是精确字符串 `ORCHESTRATOR` 或 `EXECUTOR`，`dispatch_id` 必须是 ASCII identifier；`allowed_paths` 全为 string；`invariants` 与 `gates` 为 `list[str]`；`archive_receipts` 必须是 list 且每个 receipt 的字段、identifier、candidate hash 和 boolean 类型均精确。
   - edits 的 file state 使用 strict Base64 bytes 与 mode，preimages/postimages 的 file state 使用 SHA-256 与 mode；absent state 不得携带其他字段。`gates` 只进入 envelope identity，runner 不执行 gate。

---

## 九、Review 输入与输出

普通 code review 只接收有界 baseline→current 任务 diff、SPEC、验收标准和必要上下文。
reviewer 只返回 findings；SENIOR_REVIEWER 只返回 assessment/findings；SCOUT 只返回
上下文。严重度、verdict 和范围建议都不自动生效，由 ORCHESTRATOR 独立核验和裁决。

译文语境审核使用独立的 `translation_contextual_v1` 契约：冻结有序 revision、译文
快照、术语子集、邻近译文、source tags／runtime keys 和固定源码证据；输入不包含先前
finding、裁决或建议修复。

schema 4 translation implement 采用三阶段收敛：唯一最早 contextual terminal 必须是 cycle 0
的 `REVIEW/full`，冻结原始完整有序 keys 与 source；所有 intervening terminal 只允许
`RE_REVIEW/full|closure`，但失败的历史 `FINAL_REVIEW/full` 可在更高 cycle 的
`RE_REVIEW/full|closure` 修复序列后保留。closure 使用普通七键 v1 子集 envelope，keys 必须与 inclusion 相等、
保持原顺序且 source 不漂移，并绑定最新更早 full identity。不确定时回退 `RE_REVIEW/full`。
唯一最新 terminal 必须是 STATE.cycle 的成功 `FINAL_REVIEW/full`，覆盖最新候选的原始完整 keys
与 source；失败 terminal 同样参与顺序。该最终 full 是 correctness backstop。
REVIEWER 的三行动态 prompt 仍只有 candidate identity 与 input path，不注入 prior findings、
stage data、裁决或建议修复。

接受过的 revision 仅可因有证据的 fidelity、completeness、grammar、terminology、runtime 或
conspicuous translationese 缺陷 reopen；preference churn 只作 advisory，不能扩张 closure。

Before freezing or hashing a translation_contextual_v1 payload, ORCHESTRATOR must run the deterministic offline contextual-anchor preflight with the task-scoped `.ai/task/<task_id>/SCOPE.json` and the exact seven-key draft payload.
The identical preflight is mandatory before freezing or hashing a translation_contextual_v2 full-workset draft; an unknown contextual contract still fails closed.
The preflight also accepts the whole-section form for sections without actual chapter-title t(...) calls.
The task-scoped SCOPE.json must declare only workspace-relative ordinary allowed files plus file, section_path, and ordered actual chapter-title anchors; unsafe, duplicate, missing, or ambiguous declarations fail closed.
An anchor scope may instead declare ordered_titles: [] only when its section contains no actual chapter-title t(...) calls; a titled section with [] fails closed and must declare explicit anchors.
Each declared anchor window begins at its actual chapter-title t(...) call and ends at the earliest later actual chapter title, later section marker, or EOF, so undeclared titles still bound the window.
For ordered_titles: [], the window is the whole section from its section marker to the earliest later section marker or EOF.
ORCHESTRATOR may freeze the payload only after every translation_snapshot source is proven to be the decoded first argument of a real t(...) call inside a declared anchor window; the preflight adds nothing to the payload, candidate_identity, review JSON, or STATE closure identity.
The same source proof applies to a whole-section window, and the preflight adds no payload or identity fields.
The preflight requires each translation_snapshot entry whose matching in-window t(...) call has args_order to disclose the exact canonical token args_order={i,j,...} in bounded_context.context, rejects any args_order= token when the call has none, and fails closed when matching calls disagree.

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

schema 4 translation implement 每个 cycle 还必须在 contextual 派发前重跑 preflight，并运行
strict lint、scope/source/tag/args/special/markup/placeholder/newline 不变量与
`git diff --check`。五步门禁及完整 `tools/ci-gates.sh` 只在最终 `FINAL_REVIEW/full` 收敛后运行。

完成前：

- 所有 contract 已完成且 findings 已裁决；
- implement 模式无 open accepted finding；
- 最终 AC 与适用门禁通过；
- 旧用户改动、历史 task 和 archive 未被改写；
- DONE、STOP 或明确回退前，未创建任何 child，或全部 `child_dispatches` 已确认归档。

schema 4 translation implement 的 DONE 还跨 `review_records` 与 `senior_review_records` 扫描
全部 contextual terminal 记录（包括失败）。每个记录 cycle 都不得超过 STATE.cycle 或
max_cycles；唯一最早记录必须是 cycle 0 的 `REVIEW/full`，intervening 记录只允许
`RE_REVIEW/full|closure`，或允许失败的历史 `FINAL_REVIEW/full` 后接更高 cycle 的
`RE_REVIEW/full|closure` 修复序列；唯一最新记录必须是 STATE.cycle 的成功
`FINAL_REVIEW/full`，并覆盖
最早 full 冻结的完整有序 keys 与 source。closure、stale PASS、乱序 phase、最大 tuple 平局、
越限记录或更新的失败记录均不能关闭。

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
3. `translation_contextual_v1` 仍保持原结果 schema 和冻结 envelope，现有 task 不迁移；
   `translation_contextual_v2` 是仅供 schema 5 新 task 使用的 compact lane 路由；
   `translation_surface_screen_v1` 是仅供 schema 5 新 task 使用的表层筛查路由，结果只是
   `OK|ISSUE` observation，不改变任何既有译文审核语义；
4. CLI／MCP 只作为等价传输；运行时选择只可按第 19 条形成非规范性审计观测；
5. 历史 task、review artifact、archive 和质量 evaluator 预注册不被重写；
6. 文档之间的 role／purpose／lineage 语义一致，Markdown 和 `git diff --check` 通过。
7. 禁止 runtime tuple 的预注册／持久化，但允许 reviewer 创建／恢复时的有界 live comparison
   以及仅由其产生的 `author_provider_resolution`／`model_diversity_verified` operational
   provenance，并允许第 19 条 exact-schema `runtime_observation` 审计例外；二者均不进入
   candidate 或 review identity，观测也不参与路由或完成谓词。

---

## 十三、修订记录

| 版本 | 状态 | 内容 |
| --- | --- | --- |
| `2.12-draft` | 设计草案 | 增加完成即归档、保留 dispatch 记录、不可变身份字段、持久化 `archive_attempts_started` 预算与原地更新生命周期字段；明确 `archive_pending` 在外部归档状态解决并确认前必须停留 `WAIT_USER`，拆分创建歧义发现、已知终态 reconciliation 与 active 恢复，明确语境重试保留候选／输入但更换 dispatch／agent，并要求 `DONE`／`STOP` 前完成全部归档。 |
| `2.13-draft` | 上一版草案 | 固定 `lifecycle` 与 canonical persisted role literals，保留 reader alias；记录路径数组、dispatch-to-review 绑定、NUL 分隔的候选身份和离线 `DONE`／`STOP` closure checker 及 B-prime adoption boundary。 |
| `2.14-draft` | 上一版草案 | 增加可恢复的 `candidate_author_agent_id`、归档 metadata 核验和 `author_provider_resolution` 三值枚举；明确 unavailable 的软偏好语义、reviewer child 的 operational field 分类，以及第二 reviewer 创建时的 `model_diversity_verified` 证明、碰撞 fresh retry 和 exact-identity 不可用时的 `WAIT_USER`。 |
| `2.15-draft` | 上一版草案 | 增加冻结／哈希前的离线 contextual-anchor preflight：任务作用域 SCOPE、实际 chapter-title 边界和 source-within-window 证明；它不改变 reviewer 可见的七键 payload 或任何 identity。 |
| `2.16-draft` | 上一版草案 | 增加条件性 EVIDENCE-RECONCILIATION.json、确定性 inventory/render/check/check-audit，以及 DONE 的 sidecar 候选绑定、引用一致性、前瞻性 presence、reviewer/orchestrator 身份不等和 scope-audit 复合引用检查。 |
| `2.17-draft` | 上一版草案 | 扩展 contextual-anchor preflight：无实际 chapter-title 的 section 可用 `ordered_titles: []` 声明 whole-section window；含 chapter-title 的 section 对空数组 fail closed，且不改变 payload 或 identity。 |
| `2.18-draft` | 上一版草案 | 要求 `translation_snapshot` 条目的 in-window `t(...)` 调用若带有 `args_order`，必须在 `bounded_context.context` 披露规范 token，并对缺失、错误、无关或歧义的 disclosure fail closed。 |
| `2.19-draft` | 上一版草案 | 增加受管 Phase 1 wave：唯一跨 workspace 直系 child 拓扑、角色写权限、WAVE-only CLI、pinned-manifest primary／空 collateral 重算、no-change TARGET-PATCH 能力边界、prospective／evidence／publication 恢复和外部 DONE closure。 |
| `2.20-draft` | 上一版草案 | 把 workspace ID 绑定到显式 1:1 real-worktree root map；逐调用解析 base/current/candidate 与组合 envelope；由 workset 重建非空 runtime／narrative provenance；wave STATE 持久化 parent/task/purpose；增加 prepare-publication／原子 publish，并把 done 收窄为发布后 closure。 |
| `2.21-draft` | 上一版草案 | 收紧 Phase 1 no-change 全文件字节闭合、空 content-diff、最新唯一 full completion、apply 前 integration 身份／授权／EXECUTOR provenance，以及 child agent 与 orchestrator 身份分离。 |
| `2.22-draft` | 上一版草案 | 把最新 full completion 扩展到两个 STATE review 数组和全部合法 review phase；apply 强制实际 `PASEO_AGENT_ID`；wave evidence 强制 fresh 专用 EXECUTOR 与 path/prospective identity；从固定 manifest 及 lane 冻结输入机械重建 integration source/context/terminology/briefing provenance。 |
| `2.23-draft` | 上一版草案 | 为 schema 4 translation implement 增加 v1 七键 full／closure／final-full 收敛、三轮默认上限、accepted revision reopening 门槛、分层门禁和最新 terminal full DONE 闭合；schema 3 与 review-only 保持兼容。收紧 bounded EXECUTOR：拒绝 `.git`／`.ai`／`.artifacts` 目标 namespace、非规范 POSIX 路径别名和祖先／后代目标重叠，以 preparation identity 和严格 artifact tree 恢复首个 journal 前崩溃，支持精确保持 `0o000`／`0o200` 等 owner-unreadable mode 的 hash 复验与回滚，保证恢复期 `applied_paths` 始终按目标顺序持久化，并避免读取异常被重复关闭 descriptor 掩盖。 |
| `2.24-draft` | 上一版草案 | active role prompt 改为稳定 clause ID 加角色本地触发语；新增 child dispatch 的 exact-schema `runtime_observation`，原样区分 present/null/missing，且明确排除路由、候选、review 与离线完成谓词。 |
| `2.25-draft` | 当前草案 | 追加 `translation_surface_screen_v1`（`P2-TRANSLATION-SURFACE-V1`）：schema 5 review-only surface screen 筛查契约，双层 entry 身份、q/r 四 lane batching、canonical 零项与 pre-manifest carry-over artifact、整组发布、raw bytes 绑定与封闭机器 reason_code 的 append-only ledger；surface 结果只是 `OK|ISSUE` observation，不宣称 deep review 或 repair 完成，也不借用 contextual 的 implement 收敛。 |

## `P2-TRANSLATION-CONTEXT-V2`

`translation_contextual_v2` 只用于 `schema_version >= 5` 的新 task，不能和 v1 混用；v1 历史
schema、fixture、hash 与收敛规则不迁移。v2 七键 payload 由固定 expected contract 的 validator
以 canonical UTF-8 JSON 绑定 candidate identity；不可信 payload 不能自选 validator。

总 revision 不少于四条时可冻结恰好四个 contiguous balanced lane 及权威
`CONTEXTUAL-LANE-GROUP-<group_id>.json`。manifest 绑定 task、phase、cycle、attempt、完整 workset、
四条 dispatch/path/hash；四个不同 direct-child REVIEWER 使用 `contextual_reviewers` 数组及
dispatch/labels 的 group/index immutable binding。四 lane 是一个 stage，不消耗四个 cycle，
也不适用同候选配对 code review 的 model-diversity 规则。partial group 不发布；retry 全组使用
更高 attempt。

每个接受的 v2 record 绑定 `.ai/reviews/<task_id>/raw-<dispatch_id>.txt` exact bytes 及 SHA-256；
DONE checker 重新严格解析，拒绝 duplicate keys、BOM、非法 UTF-8、非标准常量和附加字节。
terminal 使用 `(cycle,attempt,member_ordinal)`，lane stage 恰含 1..4，full/closure 恰含 0。
closure 以 `parent_review_kind` 和 `parent_coverage_identity` 绑定最新更早 full coverage。
`FINAL_REVIEW` 只允许 whole-workset full，负责跨条术语、专名和关系一致性；lane 永不关闭任务。
prompt 模板和实例 UTF-8 bytes 均不得超过 800。完整 payload/result/raw/manifest/recovery/外发规则
以 `docs/paseo-translation-context-review-v2-contract.md` 为准。

## `P2-TRANSLATION-SURFACE-V1`

`translation_surface_screen_v1` 只用于 `schema_version >= 5` 的 review-only 新 task，不能与
`translation_contextual_v1`/`v2` 或其他译文契约混用；完整规则以
`docs/paseo-translation-surface-screen-v1-contract.md` 为准。它实现生产收敛 SPEC 中
surface-screen 任务的最小 pilot：双层 entry 身份
（`logical_entry_identity` 跨版本稳定主键 + `entry_revision_identity` 版本化 revision）、
canonical bytes、仓库相对 POSIX 路径与 extractor-stable 非行号 `call_locator`（拒绝嵌入的
file:line 形式）都由 strict validator 重算，不匹配即 fail closed。

batching 是全定义算法：`n=0` 不 dispatch，改以 canonical 零项 artifact
`SURFACE-SCREEN-ZERO.json`（恰含 contract、task_id、`screen_count=0`、
`proves_no_surface_dispatch=true`、`reason="zero/no-dispatch"`、`algorithm` 与可重算的
empty-workset/input snapshot `workset_identity`，且不得声明任何 dispatch 输入）证明未发生
任何 surface dispatch；`1..3` 用单一 full 成员；`4..80` 冻结四个 contiguous q/r lane
（`q=floor(n/4)`，前 `r=n mod 4` 条多一项，无空 lane，ordered union 精确等于 screen 集合）
及权威 `SURFACE-SCREEN-GROUP-<group_id>.json`；`n>80` fail closed，必须先用
`split_carry_over` 在 manifest 构造前形成并落盘 canonical pre-manifest carry-over artifact
`SURFACE-SCREEN-CARRY-OVER.json`（绑定原始有序 workset、first-80 screen 集、剩余有序
carry-over、计数与 `surface-carry-over/1` 算法版本），carry-over 绝不得记为完成；DONE 必须
用 strict validator 重检该 artifact，并要求 STATE 绑定指向原始冻结 workset 的输入路径，
使 screen+carry 有序拼接逐项等于原始冻结身份集，任何 omit/extra/overlap/计数篡改 fail
closed。四条 lane record 只能整组发布；任一失败归档全组并以更高 attempt fresh retry（fresh
IDs，surface manifest/group 只允许 `REVIEW` phase，从不出 RE_REVIEW）。每个接受的 record 绑定
task/dispatch 推导的 raw bytes 与 `raw_output_sha256`，并持久化与 STATE/dispatch 相等的
`workspace_id`、`parent_agent_id` 和 literal `lineage_verified=true`；DONE checker 重算并重新
严格解析；dispatch/labels/record/envelope 四方 identity/path/index 逐字相等，
`candidate_identity` 冻结后不可变。surface 的独立 whole-screen terminal 是恰一个覆盖
1..3 项（full）或至多 80 项（lane_group）的成功 `REVIEW/full` 或 `REVIEW/lane_group`
stage（或零项 artifact），不借用 contextual 的 implement RE_REVIEW/FINAL_REVIEW 收敛；已
dispatch 的 surface 不能用 STOP 关闭——该拒绝绑定在 dispatch 自身的 purpose 字段上，篡改
review_contracts 或 schema_version 也不能恢复 STOP。surface 任务必须使用
`change_class=translation_workflow`，并在 STATE 携带独立的不可变 surface evidence
reconciliation binding（算法版本 + terminal 类别 + 终端 artifact 路径→SHA-256 精确映射），
DONE 从当前字节重算该绑定，漂移、缺失或 terminal 不符 fail closed；该绑定独立于
code/contextual sidecar terminal，但存在真实 code record 时 sidecar reconciliation 绝不豁免。

surface 结果逐项只是 `OK|ISSUE` observation：`ISSUE` 必须经 ORCHESTRATOR 按固定源码裁决才
能成为 finding，`OK` 不得写成 `deep_reviewed` 或 `closed`；surface terminal 只记录 surface
completion，不宣称 deep review 或 repair 完成。长期 entry-revision 状态由 append-only
ledger 工具按生产 SPEC 的命名状态机独立校验：每条迁移携带封闭集机器 `reason_code` 与不可
变 snapshot/handoff `provenance`（kind+SHA-256），且每个具名 `(from_state,to_state)` 迁移
绑定其允许的 provenance kind 集合；invalidation 只接受身份变化原因（含逻辑迁移原因
`call_locator_changed`／`source_tag_changed`），逻辑迁移的后续新逻辑身份 revision 必须紧随
其 invalidation 记录并携带指回它的显式 migration edge，closed revision 只能因身份变化进入
新 revision 或因新的 fidelity/completeness/grammar/terminology/runtime/translationese 证据
reopen，偏好不得 reopen；ledger 只追加不重写，任意位置重复不可变事件与跨逻辑身份的
revision 复用 fail closed（仅 exact last line 幂等），且禁止从 provider/model 名称推导任何
覆盖、稳定性或完成度。
