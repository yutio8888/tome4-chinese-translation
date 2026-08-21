# ORCHESTRATOR briefing（Paseo 轻量编排）

本文件用于 Paseo 大型任务。AGENTS.md 是上位规则；本文件只说明最小操作流程。

## 职责

ORCHESTRATOR 负责定义范围、委托实现、独立验证、裁决 finding 和向用户交付。EXECUTOR
是任务内容文件的唯一写入者；ORCHESTRATOR 可以同时更新当前 task 的编排记录和验证
工具产生的忽略产物。

## 角色独占路由

从任务建立 Paseo task ID 到 DONE、STOP 或明确回退期间，不使用已归档旧项目 Skill
（$tome4-pi-review、$tome4-pi-file-review、$tome4-pi-subagent，见 archive/），也不
调度它们的独立 reviewer、scout 或 plan-reviewer。计划和源码核验由 ORCHESTRATOR
完成，任务内容写入只交给 EXECUTOR，代码／工具／文档复审只交给 REVIEWER 和
SENIOR_REVIEWER；只读源码侦察可交给 SCOUT。角色规模过小或不需要委托时由
ORCHESTRATOR 直接完成。

门禁和普通检查仍是 ORCHESTRATOR 可直接调用的工具；直接运行这些工具不等于启用已归档
Skill。已归档 Skill 产生的 review 结果不得用来完成 Paseo 的 code_legacy_v1、REVIEW
或 FINAL_REVIEW。

## 开始任务

1. 选取新的 task_id，使用 .ai/task/<task_id>/ 与 .ai/reviews/<task_id>/；不得覆盖旧任务
   或 legacy flat 记录。
2. 记录 git status --short。任务前脏文件默认不交给 EXECUTOR；确需修改时逐文件写入
   SPEC，并保存 tracked 文件的 BASELINE.patch 或既有 untracked 文件的 baseline/副本。
3. 明确模式、允许修改文件、禁止扩展项和可验证验收标准；将任务分类为 standard、
   translation_workflow 或 infrastructure。后两类自初审起必须交叉复审。
4. 每次 child 调度前，ORCHESTRATOR 必须读取实时 `list_profiles`，结合 profile notes 与当前
   provider/model 能力选择适用 profile；这里只记录 role、purpose、workspace、lineage
   和候选绑定，不把运行时组合写入 STATE、candidate identity 或 review contract identity。
   同一 provider 的另一个 profile 只能是复杂度升级，不能在该 provider 已不可用时充当 availability fallback。

5. 角色按下表创建，不固定执行载体：

   | role | purpose | 责任 |
   | --- | --- | --- |
   | executor | — | 实现 SPEC |
   | reviewer | normal_review | 代码、工具、测试和文档复审 |
   | reviewer | translation_contextual_v1 | 译文语境审核 |
   | senior-reviewer | cross_review / scope_audit | 交叉复审或范围校准 |
   | scout | source_scout | 只读源码侦察 |

6. 确认当前进程存在非空 PASEO_AGENT_ID。若缺失，不得创建子 agent，应报告当前主代理
   不是 Paseo 托管 parent。
7. 在当前 task 目录写 SPEC.md、简短 PLAN.md 和最小 STATE.json；若选择 translation_contextual_v1，冻结前另写任务作用域 SCOPE.json 并运行其离线 anchor preflight。任务开始时选定
   orchestration_transport（只允许 cli|mcp），任务内不切换；CLI 与 MCP 必须保持相同
   role、purpose、workspace、lineage、label 恢复、reviewer 只读与候选一致性语义：

~~~json
{
  "schema_version": 2,
  "task_id": "...",
  "mode": "implement",
  "change_class": "standard",
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
  "senior_reviewer": {"role": "senior-reviewer", "purpose": null, "agent_id": null},
  "child_dispatches": [],
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": [],
  "senior_review_records": [],
  "wait": null,
  "last_error": null,
  "updated_at": "..."
}
~~~

已创建 child 的持久化条目使用相同的 canonical role literal，例如
`{"role":"REVIEWER","lifecycle":"archived","archive_confirmed":true}`；运行时
派发 label 仍使用小写 `reviewer`。

contextual_reviewer 和 scout 是条件字段：只有任务实际选择对应 role/purpose 时才写入。
语境派发后，candidate_identity、dispatch_id、input_path 和 agent_id 必须非空并与当前
冻结候选一致。`child_dispatches` 初始为空；每次创建成功后追加 role、purpose 和非空
agent_id；语境 REVIEWER 的记录还保存 candidate_identity、dispatch_id 和 input_path。
新持久化 dispatch 只写 `lifecycle`（不写 `status`）及 `EXECUTOR`、`REVIEWER`、`SCOUT`、
`senior-reviewer` 四个 role literal；运行时 `labels.role` 继续使用小写值。reader 可读取
既有 `status`／小写 role alias，但不得把它们重新写入。以上身份字段都不可改写，只在原记录更新 lifecycle、archive_confirmed、
持久化 canonical role 集合为 `EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer`。
archive_attempts_started、last_error 和 archived_at。archive_attempts_started 初始为 0、
最大为 2；每次递增都在外部调用前立即持久化。STATE 不记录执行载体、版本、档位或回退
元组。provider、model、mode、thinking 和 fallback tuple 不写入 STATE、candidate identity
或 review contract identity。

Before selecting any reviewer profile, ORCHESTRATOR must freeze the implementation candidate, re-enumerate the task's allowed changed paths, and persist candidate_author_agent_id in the task-scoped `.ai/task/<task_id>/STATE.json` at that freeze/path-re-enumeration event.
The persisted candidate_author_agent_id must point to the latest accepted output that was produced or materially changed by the current task's lineage-verified EXECUTOR, not to an author inferred from another task's STATE.
When the candidate changes, ORCHESTRATOR must recompute candidate_author_agent_id before the new review dispatch; it is immutable within a freeze, and ORCHESTRATOR must not traverse another task's STATE to invent it.
candidate_author_agent_id is null for review-only work and for an implement candidate that predates any managed EXECUTOR.

冻结实现候选时，ORCHESTRATOR 在选择任何 reviewer profile 前，于任务作用域 `.ai/task/<task_id>/STATE.json` 的现有冻结／路径
重枚举事件写入 `candidate_author_agent_id`。它必须是当前 lineage 已核验 EXECUTOR 的稳定
直接 `agent_id`，且指向最近一次产出或实质改变该冻结候选的已接受输出；候选改变时重新计算，
同一冻结候选内不可改写，不得遍历其他任务的 STATE。review-only 或早于任何受管 EXECUTOR
的实现候选将其置为 `null`。每个候选绑定的 REVIEWER／SENIOR_REVIEWER dispatch 复制同一
指针；副本不可改写，且不进入 candidate_ref、candidate_identity、review JSON 或 review
contract identity。
The immutable per-dispatch author pointer is copied to every candidate-bound reviewer dispatch and cannot be rewritten within that dispatch; it is excluded from candidate_ref, candidate_identity, review JSON, and review-contract identity.

只有对应 reviewer 的 `child_dispatches` 条目记录
`author_provider_resolution=verified|unavailable|not_applicable`，不写 review JSON；它是可
更新 operational field，而指针是 immutable candidate field。该 enum 只在 child 创建／adoption
已无歧义后记录；ambiguous-create reconciliation 与 recovery 都要在使用前重新解析，暂时缺
enum 本身不触发 `WAIT_USER`。`not_applicable` 是统一值，
Only the corresponding reviewer entry in STATE child_dispatches records author_provider_resolution=verified|unavailable|not_applicable; review JSON excludes this enum, which is recorded only after unambiguous child creation or adoption and re-resolved before using a recovered reviewer dispatch.
After ambiguous-create reconciliation or recovery, ORCHESTRATOR must re-resolve author_provider_resolution before using the dispatch, and a temporarily missing enum alone must not force WAIT_USER.
只用于 review-only、早于受管 EXECUTOR 的实现候选，或无冻结代码候选的 `scope_audit`。每次
reviewer 派发（含恢复）都按该指针查询包含 archived agent 的实时 Paseo metadata，在消费
显式 provider 前核验 agent id、workspace、task／role label、parent lineage 和 EXECUTOR role。
查询基础设施最多重试一次；作者记录缺失，或 agent id、workspace、task／role label、parent
lineage、EXECUTOR role 任一身份核验失败，均在一次重试后记录
`author_provider_resolution=unavailable`；显式 provider 缺失或表示不同也同样记录
`unavailable`。Before consuming the transport's explicit provider, ORCHESTRATOR must query live Paseo metadata including archived agents and verify the author agent id, workspace, task/role labels, parent lineage, and EXECUTOR role.
If the author record is missing, any of the author agent id, workspace, task/role labels, parent lineage, or EXECUTOR role checks fails, or the explicit provider is missing or differently represented, retry the lookup once, then record author_provider_resolution=unavailable without inferring a provider. 这是诚实的软偏好
失败，说明作者 provider 避让不可执行但仍可继续合格 dispatch；不得使用主要订阅 provider
例外，也不得从 memory、profile 名称、title 或 heuristic 推断。只有 `verified` 才允许该
例外；它只证明 lookup 与身份检查成功，不证明选中了不同 provider。归档保留期之外不可恢复
的情况保持 `unavailable`，不伪造作者信息。
The same-provider budget exception is allowed only when the author-provider resolution is verified; unavailable resolution remains a soft preference failure.
not_applicable is used for review-only work, implement candidates predating any managed EXECUTOR, and scope_audit with no frozen code candidate.

第二个配对 reviewer 创建时，实时取得两名 reviewer 的精确 model identity，第一名即使已
archived 也必须查询；仅在核验两者不相等后，才在两条 reviewer child dispatch 上写入
`model_diversity_verified=true`。该值与 resolution enum 都是可更新 operational fields，
不是 runtime tuple 或持久化 identity；有效的 true proof 只适用于完整且成对的记录。若模型
碰撞，先按普通归档纪律归档第二个 child，再以 fresh child 重试。When paired reviewer exact model identities collide, archive the second child before creating a fresh retry child, preserving the role, purpose, workspace, lineage, and candidate binding.
At creation of the second reviewer, ORCHESTRATOR must obtain both live exact model identities, verify exact inequality, and only then persist literal `true` for model_diversity_verified on both reviewer dispatch entries.
If either exact model identity remains unavailable after one retry, enter `WAIT_USER` and do not infer identity from provider, profile, title, memory, or enum.
If a second reviewer exists or was unambiguously adopted but either `model_diversity_verified` proof is missing or partial, re-resolve both exact model identities once; persist literal `true` on both entries when they differ, archive the second child and fresh-retry on collision, and enter `WAIT_USER` if either identity remains unavailable.
不得从 provider、profile 名称、title、memory 或 enum 推断。明确删除的复杂度禁止 runtime tuple 预注册／持久化，但允许这里有界的 live
comparison 与 derived operational provenance。
Operational author_provider_resolution and model_diversity_verified fields are excluded from runtime tuples, candidate identity, review-contract identity, review JSON, and offline STATE-checker closure predicates.

审核路由还必须满足以下运行时无关规则：reviewer 尽量避开候选作者的 provider；候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核，但仍须满足 role、purpose 和
候选边界。同一交叉审核阶段的两名 reviewer 必须使用不同的精确 model identity，且不同
provider 优先；无法组成不同 model 时不得猜测，进入 `WAIT_USER`。任何 fallback 都必须
创建 fresh child，并保持 role、purpose、workspace、parent lineage 与 candidate binding
不变；不得 resume 已完成或已归档 child。

所有 EXECUTOR、REVIEWER、SENIOR_REVIEWER 和 SCOUT 都必须由当前 ORCHESTRATOR 进程
直接创建：CLI 使用 Paseo run，MCP 使用 agent-scoped 的 create_agent。创建载荷至少
包含 workspace、task／role label 和初始 briefing；不要通过另一个 agent 创建子 agent。
daemon 必须以 ORCHESTRATOR 建立 parent lineage，不能手写 parent label。

## 实现与验证

为 EXECUTOR 生成自包含 briefing，至少包含 SPEC、PLAN、允许文件、任务前改动和验收命令。
使用完整 task/role label 创建 agent；创建参数中与当前 Paseo 接口有关的其他字段由
运行时环境提供，不属于本契约。

取得精确 agent ID 后立即核验：

1. agent 属于 STATE 的 workspace_id；
2. labels.task_id、labels.role 和需要的 labels.purpose 精确匹配；
3. parent lineage 的 ParentAgentId 或 paseo.parent-agent-id 精确等于
   orchestrator_agent_id；
4. EXECUTOR 是唯一活动写入者；
5. REVIEWER、SENIOR_REVIEWER 和 SCOUT 运行前后工作树没有变化；
6. 语境 REVIEWER 的 candidate_identity、dispatch_id 和 input_path 与冻结候选一致。

PASEO 状态面无法暴露可验证 parent lineage 时，停止该 child 并进入 WAIT_USER。任一
角色、purpose、workspace、lineage 或权限检查失败，都不得把输出记为有效审核结果。

每次 child dispatch 都是单次运行。child 到达终态后，先收获输出并验证为有效或判为无效，
再立即使用当前 transport 的 `paseo archive`／`archive_agent` 归档并核验归档状态。每次
归档调用前先持久化递增 archive_attempts_started；递增后崩溃或结果不明确也视为消耗该次
预算，恢复时先只读查状态。只有 archive_confirmed=true 才算 dispatch 完成，才可推进阶段
或创建 successor；已归档 child 不得 resume 或 send follow-up。无效输出同样先归档，再
创建 fresh retry。

### SCOUT 源码侦察

需要源码核验但希望并行委托时，创建 fresh SCOUT，labels 含 task_id、role=scout 和
purpose=source_scout。briefing 写明组件、公开源码根路径与机制问题，并引用
.ai/roles/scout.md 的输出 schema。SCOUT 输出只作上下文，不产生 finding，也不作为
review contract 结果；完成后收获输出并立即 archive。同一任务同时最多一个活动 SCOUT。

同一 workspace 只运行一个 EXECUTOR。完成后由 ORCHESTRATOR 收获回报，检查实际 diff、
越权文件和相关测试，随即归档该 EXECUTOR；归档确认后才进入 VALIDATE。后续 FIX 创建
fresh EXECUTOR，不向已归档会话发送 follow-up。若任务修改既有脏文件，用保存的起始
patch／副本生成 baseline→current 任务自身 diff，确认用户原有内容未被意外覆盖。

是否需要终止性探针以实际 diff 为准。若实现重构了可能阻塞测试进程的扫描／解析循环，
先取得进度不变量说明并运行短超时、有限输入探针，再运行更广测试。挂起、持续增长输出
或 OOM 时先终止子进程，不得无界重跑；仍无法归因时进入 WAIT_USER。

## 复审与裁决

每个 code review phase 首次派发前冻结 SPEC、diff 生成配方、候选路径集和任务自身 diff。
路径集只包含 SPEC 允许且相对任务基线实际变更／新建的任务内容；candidate_ref 精确为
`SHA256(SPEC 原始字节 + 一个 NUL 字节 + diff 原始字节)`。派发、返回和 contract 完成前重新枚举路径集，路径集或
配方变化即重建候选。

代码、工具和文档由 role=reviewer、purpose=normal_review 接收有界 diff、SPEC 和必要
上下文；SENIOR_REVIEWER 在 cross_review 时接收同一份 SPEC 和 diff，二者返回前不得互看
findings。译文语义审核由 role=reviewer、purpose=translation_contextual_v1 按独立契约
接收冻结 envelope；不得把历史 finding 注入其中。

Before freezing or hashing a translation_contextual_v1 payload, ORCHESTRATOR must run the deterministic offline contextual-anchor preflight with the task-scoped `.ai/task/<task_id>/SCOPE.json` and the exact seven-key draft payload.
The task-scoped SCOPE.json must declare only workspace-relative ordinary allowed files plus file, section_path, and ordered actual chapter-title anchors; unsafe, duplicate, missing, or ambiguous declarations fail closed.
Each declared anchor window begins at its actual chapter-title t(...) call and ends at the earliest later actual chapter title, later section marker, or EOF, so undeclared titles still bound the window.
ORCHESTRATOR may freeze the payload only after every translation_snapshot source is proven to be the decoded first argument of a real t(...) call inside a declared anchor window; the preflight adds nothing to the payload, candidate_identity, review JSON, or STATE closure identity.

review 记录必须标明 task_id、review_contract、review_phase、cycle、attempt、reviewer_role、
purpose、dispatch_id、agent_id 和结果。STATE 的 review_records 与 senior_review_records 新写入为
workspace-relative review 文件路径数组；读取旧 mapping 时只作兼容。语境记录还要标明 candidate_identity、dispatch_id 和 input_path。
每个 code review 记录保存 candidate_ref 及恰含 spec_path/diff_path 的 candidate_locator；不一致时不得合并输出。每个 REVIEWER 或
SENIOR_REVIEWER 返回后，先独立保存并校验其输出，再立即归档该 child；一方归档不向仍在
运行的另一方泄露结论。只有所需输出及其归档状态全部确认后，review contract 才完成。
准备进入 DONE 或 STOP 时，调用 `python3 -B tools/ai_state_check.py STATE.json`（非终态
preflight 显式传 `--target DONE|STOP`）。它只读取持久化 STATE、review record 和冻结输入；
`STOP` 只要求无 child 或每个 child 的规范化 lifecycle 为 `archived` 且 `archive_confirmed`
为 literal `true`。A child counts as archived only when its normalized lifecycle is `archived` and `archive_confirmed` is literal `true`.
历史 task-id 是否信息性跳过只由 tracked `.ai/legacy-cohort-manifest.json` 的
`unsupported_tasks` 边界决定，缺失新字段不是回退条件。

## 修复与完成

每轮把全部 accepted findings 按依赖顺序交给 fresh EXECUTOR，修复后收获回报并立即
归档，再重新验证和复审。自动修复最多五轮；相同问题持续存在时可以更换新的 EXECUTOR，
也可以询问用户。

当 cycle >= 2 且普通 review finding 触发 FIX 时，先完成当轮 scope_audit；客观验证失败
直接触发的 FIX 不需要 scope audit。修复后的验证通过进入 RE_REVIEW。

review_only 在全部 contract 完成、findings 已裁决且无 deferred 后进入 DONE。implement
还要求无 open accepted finding 且最终验收通过。需要决定时进入 WAIT_USER；取消或无法
继续时，只有尚未创建 child 或全部 child 已确认归档才进入 STOP，否则进入 WAIT_USER。

## 失败恢复

查询、wait 或 send 的临时错误可以重试一次。恢复严格分三步：

1. 创建结果不明确且本地尚无 agent_id 时，直接按 workspace／cwd、labels.task_id、
   labels.role、需要的 labels.purpose、lineage 和候选绑定过滤传输结果；先排除已记录的历史
   agent_id，但不按远端 lifecycle 排除尚未记录的结果，过滤先于基数判定。无匹配可重试创建
   一次；唯一匹配且身份正确时，无论状态如何，先追加完整不可变身份、观测 lifecycle 与初始
   生命周期字段到 child_dispatches。只有 active 才更新当前角色字段并复用；archived 先
   核验并记录 archive_confirmed=true，且不得重试创建；terminal／stopping／archive_pending
   记录按已保存 agent_id 转入 lifecycle reconciliation。多个匹配、截断列表或无法
   唯一确认时进入 WAIT_USER，不得盲目创建第二个写入 agent。
2. 重启恢复先按 child_dispatches 的已知 agent_id reconciliation 所有未确认归档记录：
   terminal 输出先收获／判废，再根据 archive_attempts_started 的剩余预算 archive；stopping
   先确认终态再 archive；archive_pending 只读核验状态。处理完之前不得恢复 active 会话或
   创建 successor。
3. 最后只恢复当前角色字段指向的唯一 active dispatch；排除 archived、terminal、stopping、
   archive_pending 和其他历史记录，再核验 role、purpose、workspace、lineage 与候选绑定。

归档首次尝试和一次自动重试合计最多两次，每次调用前持久化递增
archive_attempts_started。状态查询仍未归档且计数为 1 时才可重试；计数达到 2 后仍无法确认
则标记 archive_pending，记录 last_error 和 wait，进入 WAIT_USER，不推进阶段或创建
replacement。取消运行中 child 时先 stop／cancel 并核验终态，再 archive。更换普通 child
保持相同 role、purpose、workspace、lineage 和候选绑定；语境 REVIEWER 则保持同一
candidate_identity 与冻结 input_path 字节，同时分配新的 dispatch_id 和 agent_id。旧输出
作废且不得混合；语境 REVIEWER 每次新派发、重跑和无效输出重试都不能复用旧会话。

进入 DONE、STOP 或明确回退前 reconciliation 全部 child_dispatches；只有尚未创建任何
child，或所有 child 都已确认归档，才可结束／回退。Paseo 不可用但仍有未确认归档 child
时进入 WAIT_USER，不得退出编排后由主代理继续；没有 child 或已全部归档且用户未强制要求
Paseo 时，才可记录回退。若用户明确要求 Paseo，则报告阻塞。已归档 Skill 不参与回退路由。
