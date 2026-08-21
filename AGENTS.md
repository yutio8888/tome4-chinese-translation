# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 角色与协作

- **主代理**负责范围、裁决、验证和最终交付，通常也是仓库写入者。
- **审核子进程／项目 subagent**只返回 proposal、context 或 findings；其结果由主代理核验后再应用。
- **Paseo 编排**启用时，主代理任 ORCHESTRATOR；EXECUTOR 是任务内容文件的唯一写入 agent，REVIEWER 做常规独立复审，SENIOR_REVIEWER 做超过两轮后的范围校准和高影响流程交叉复审，SCOUT 做只读源码侦察（返回压缩代码上下文，不产生审核 contract 结果）。

无论采用哪种协作方式，模型输出都不是最终事实：机制以固定版本源码为准，修改以后文门禁和验收标准为准。
所有 finding 必须有源码或语境证据；主代理独立标为 `confirmed`、`pending` 或 `advisory`，只有 `confirmed` 可自动进入修复，模型报告的 severity 不是真实事实。

Paseo 从任务明确采用该编排并建立 task ID 时视为激活，直到任务进入 `DONE`／`STOP`，
或 ORCHESTRATOR 明确回退并记录原因。回退只允许在尚未创建任何 child，或 `child_dispatches` 全部
`archive_confirmed=true` 时发生；否则必须先 reconciliation，无法确认则进入 WAIT_USER，
不得切回主代理继续任务。旧项目 Skill（`$tome4-pi-review`、
`$tome4-pi-file-review`、`$tome4-pi-subagent`）已归档（见 `archive/`），不再参与任何审核
路由；委托、实现、源码侦察和独立复审只通过 Paseo 的
ORCHESTRATOR／EXECUTOR／REVIEWER／SENIOR_REVIEWER／SCOUT 角色完成。门禁和普通
检查仍可由 ORCHESTRATOR 作为工具直接调用，不视为启用已归档 Skill。

## Paseo 轻量编排（大型任务）

当前已核验的 Paseo 0.4.0（CLI 或等价注入的 agent-scoped Paseo MCP 操作）用于需要多步实现和独立复审的大型任务；小型修改由主代理直接完成。任务级 orchestration_transport 在 STATE 中只允许 cli|mcp，两种传输必须保持相同的 role、purpose、workspace、lineage、歧义恢复和 reviewer 只读语义。用户明确要求 Paseo 时必须使用；否则 Paseo 不可用时，只有尚未创建 child 或全部 child 已确认归档才可回退主代理执行并说明，仍有未确认归档 child 则进入 WAIT_USER。角色 prompt 见 .ai/roles/，轻量设计说明见 docs/paseo-orchestration-v2-contract.md。活跃角色或契约修改后运行 `python3 -B tools/paseo_contract_check.py`，只检查角色/purpose 约束和固定运行时身份回流。

### 最小规则

1. 同一 workspace 同时只能有一个任务内容写入 agent；EXECUTOR 运行时，ORCHESTRATOR 仍可更新当前 task 的编排记录和验证产物。
2. EXECUTOR 只改任务允许的文件，不 commit、不 stage；REVIEWER、SENIOR_REVIEWER 和 SCOUT 与其使用同一 workspace，但不得修改任何文件。
3. ORCHESTRATOR 独立核验测试和 finding，只把已接受的 finding 交给 EXECUTOR 修复；reviewer 的 severity、verdict 和范围建议都不自动生效。
4. 自动修复最多五轮。第二轮后若普通 review finding 仍要求进入下一轮 FIX，必须先由 SENIOR_REVIEWER 审查意见是否偏离设计意图、功能边界或个人项目规模；每个后续轮次都重新校准当轮意见。
5. 所有 agent 委托只使用 EXECUTOR、REVIEWER、SENIOR_REVIEWER、SCOUT；旧项目 Skill 已归档，不再调度，其输出不得计入任何 Paseo contract。SCOUT 只做只读源码侦察，不承担审核 contract、不产生 finding。
6. 译文审核由 Paseo REVIEWER 按 purpose=translation_contextual_v1 承担：有界、只读、独立记录与指标；SENIOR_REVIEWER 不承担该 purpose。语境候选冻结后先计算 candidate_identity，把外层 envelope 以紧凑 JSON 字节冻结到任务作用域 workspace 相对输入文件；initialPrompt 只携带任务、输入和输出三行的短派发 prompt。

Before freezing or hashing a translation_contextual_v1 payload, ORCHESTRATOR must run the deterministic offline contextual-anchor preflight with the task-scoped `.ai/task/<task_id>/SCOPE.json` and the exact seven-key draft payload.
The task-scoped SCOPE.json must declare only workspace-relative ordinary allowed files plus file, section_path, and ordered actual chapter-title anchors; unsafe, duplicate, missing, or ambiguous declarations fail closed.
Each declared anchor window begins at its actual chapter-title t(...) call and ends at the earliest later actual chapter title, later section marker, or EOF, so undeclared titles still bound the window.
ORCHESTRATOR may freeze the payload only after every translation_snapshot source is proven to be the decoded first argument of a real t(...) call inside a declared anchor window; the preflight adds nothing to the payload, candidate_identity, review JSON, or STATE closure identity.
7. EXECUTOR、REVIEWER、SENIOR_REVIEWER、SCOUT 必须是当前 ORCHESTRATOR 的 Paseo-managed child，并出现在其 Subagents track；创建只能走当前 Paseo 的 CLI 或 agent-scoped MCP `create_agent` 操作，不得使用其他 agent 创建接口。创建载荷必须带有任务／角色 `labels`。主代理必须有非空 `PASEO_AGENT_ID`，并在 STATE 保存不可变的 `orchestrator_agent_id`；创建或恢复后必须核验 workspace、role、purpose、parent lineage（`ParentAgentId` 或等价字段）和角色权限，无法验证 lineage 时停止并进入 WAIT_USER。
8. 角色是唯一的运行时路由约束。EXECUTOR 只承担 executor role；REVIEWER 按 purpose 区分 normal_review 与 translation_contextual_v1；SENIOR_REVIEWER 只承担 cross_review 或 scope_audit；SCOUT 只返回上下文。具体执行载体、版本、档位和回退选择不写入 STATE，不参与 candidate identity，也不作为契约验收条件。
9. 修改翻译流程或项目基础设施时，普通 REVIEWER 和 SENIOR_REVIEWER 必须从同一 SPEC、同一任务自身 diff 独立交叉审核，在两份输出都返回前不得互看结论。该 code-only 交叉审核不把译文本身交给普通 reviewer；译文语义审核走 translation_contextual_v1。
10. 每个 code review phase 冻结 SPEC 和一份独立路径的有界任务自身 diff，保持候选一致性。必要的 SPEC 修改一律视为新候选；candidate_ref 精确为 `SHA256(SPEC 原始字节 + 一个 NUL 字节 + diff 原始字节)`。每次派发、返回和完成前都要重枚举当前实际变更路径集，路径集或配方改变即产生新候选。
11. 只有实际 diff 重构了可能阻塞测试进程的扫描或解析循环，才在更广测试前要求进度不变量说明和短超时、有限输入的微型探针。挂起、持续增大输出或 OOM 时先终止并确认子进程退出，不得无界重跑。
12. 任务前脏文件默认不交给 EXECUTOR；确需修改时，SPEC 必须逐文件允许，并先保存可恢复的起始 patch 或副本。review_only 的 DONE 只要求全部审核完成、findings 已裁决且无 deferred；implement 的 DONE 还要求无未解决 accepted finding 并通过最终验收。
13. 每次 child dispatch 都是单次运行：到达终态后，ORCHESTRATOR 先收获并验证或判废输出，再立即通过当前 transport 归档；归档确认属于 dispatch 完成条件，确认前不得推进阶段、创建 successor 或恢复该 child。无效输出也先归档再 fresh retry；归档首次尝试和一次自动重试都要在调用前持久化递增 `archive_attempts_started`（最大 2），预算耗尽仍无法确认则记录 `archive_pending`／`last_error` 并进入 WAIT_USER。STATE 以 `child_dispatches` 保留不可变 role／purpose／agent_id 和可更新的 `lifecycle`／`archive_confirmed`／尝试计数；新写入的持久角色只用 `EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer`，而运行时 `labels.role` 仍为小写。语境重试保留 candidate_identity 与冻结 input_path，但使用新的 dispatch_id／agent_id。DONE／STOP 前核对所有 child 均已归档。

每次 child 调度前，ORCHESTRATOR 必须读取实时 `list_profiles`，并按 profile notes 与当前
provider/model 能力选择；只记录 role、purpose、workspace、parent lineage 和 candidate
binding，不把运行时组合写入 STATE、candidate identity 或 review contract identity。可用性
按 provider 处理：同一 provider 的另一个 profile 只能是复杂度升级，不能在该 provider 已不可用时充当 availability fallback。reviewer 尽量避开候选作者的 provider；候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核，但仍须满足 role、purpose 与候选边界。
同一交叉审核阶段的两名 reviewer 必须使用不同的精确 model identity；不同 provider 优先。
无法组成不同 model 时进入 `WAIT_USER`。任何 fallback 都必须创建 fresh child，并保持
role、purpose、workspace、parent lineage 与 candidate binding 不变；不得 resume 已完成或已归档 child。

Before selecting any reviewer profile, ORCHESTRATOR must freeze the implementation candidate, re-enumerate the task's allowed changed paths, and persist candidate_author_agent_id in the task-scoped `.ai/task/<task_id>/STATE.json` at that freeze/path-re-enumeration event.
The persisted candidate_author_agent_id must point to the latest accepted output that was produced or materially changed by the current task's lineage-verified EXECUTOR, not to an author inferred from another task's STATE.
When the candidate changes, ORCHESTRATOR must recompute candidate_author_agent_id before the new review dispatch; it is immutable within a freeze, and ORCHESTRATOR must not traverse another task's STATE to invent it.
candidate_author_agent_id is null for review-only work and for an implement candidate that predates any managed EXECUTOR.
provider、model、mode、thinking 和 fallback tuple 不写入 STATE、candidate identity 或
review contract identity。

实现候选冻结时，ORCHESTRATOR 在选择任何 reviewer profile 前，于任务作用域 `.ai/task/<task_id>/STATE.json` 的冻结事件写入
`candidate_author_agent_id`：它是当前 lineage 已核验 EXECUTOR 的稳定直接 `agent_id` 指针，
指向最近一次产出或实质改变该候选的已接受输出；候选改变时重新计算，同一冻结候选内不可改写，
不得遍历其他任务 STATE。review-only 或早于任何受管 EXECUTOR 的实现候选为 `null`。每个
候选绑定的 REVIEWER／SENIOR_REVIEWER child dispatch 复制该指针，但不把它写入 candidate_ref、
candidate_identity、review JSON 或 review contract identity。
The immutable per-dispatch author pointer is copied to every candidate-bound reviewer dispatch and cannot be rewritten within that dispatch; it is excluded from candidate_ref, candidate_identity, review JSON, and review-contract identity.

只有对应 reviewer 的 `child_dispatches` 条目记录
`author_provider_resolution=verified|unavailable|not_applicable`；这是可更新 operational
field，review JSON 不记录。该 enum 只在 child 创建／adoption 已无歧义后记录；ambiguous-create
reconciliation 与 recovery 都要在使用前重新解析，暂时缺 enum 本身不触发 WAIT_USER。
Only the corresponding reviewer entry in STATE child_dispatches records author_provider_resolution=verified|unavailable|not_applicable; review JSON excludes this enum, which is recorded only after unambiguous child creation or adoption and re-resolved before using a recovered reviewer dispatch.
After ambiguous-create reconciliation or recovery, ORCHESTRATOR must re-resolve author_provider_resolution before using the dispatch, and a temporarily missing enum alone must not force WAIT_USER.
`not_applicable` 统一用于 review-only、早于受管 EXECUTOR 的实现
候选，或没有冻结代码候选的 `scope_audit`。每次 reviewer 派发（含恢复）先查询包含 archived agent 的 Paseo metadata，核验 agent id、workspace、task／role label、parent lineage 和
EXECUTOR role，再读取显式 provider；基础设施最多重试一次，缺失或身份表示不同的 provider
记为 `unavailable`。作者记录缺失，或 `agent_id`、`workspace`、`task／role label`、
`parent lineage`、`EXECUTOR role` 任一身份核验失败，均在一次重试后记为
`author_provider_resolution=unavailable`；显式 provider 缺失或表示不同也同样记为
`unavailable`。Before consuming the transport's explicit provider, ORCHESTRATOR must query live Paseo metadata including archived agents and verify the author agent id, workspace, task/role labels, parent lineage, and EXECUTOR role.
If the author record is missing, any of the author agent id, workspace, task/role labels, parent lineage, or EXECUTOR role checks fails, or the explicit provider is missing or differently represented, retry the lookup once, then record author_provider_resolution=unavailable without inferring a provider.
该值表示作者 provider 避让不可执行的软偏好，不得宣称主要订阅 provider
例外成立；只有 `verified` 才可使用该例外，且 `verified` 不等于选择了不同 provider。
not_applicable is used for review-only work, implement candidates predating any managed EXECUTOR, and scope_audit with no frozen code candidate.
The same-provider budget exception is allowed only when the author-provider resolution is verified; unavailable resolution remains a soft preference failure.

第二个配对 reviewer 创建时实时取得两名 reviewer 的精确 model identity（第一名可已
archived），核验不相等后才在两条 reviewer child dispatch 上写入
`model_diversity_verified=true`。该值与上述 enum 都是可更新 operational fields，不是持久
runtime tuple；有效的 true proof 只适用于完整且成对的记录。
At creation of the second reviewer, ORCHESTRATOR must obtain both live exact model identities, verify exact inequality, and only then persist literal `true` for model_diversity_verified on both reviewer dispatch entries.
When paired reviewer exact model identities collide, archive the second child before creating a fresh retry child, preserving the role, purpose, workspace, lineage, and candidate binding.
If either exact model identity remains unavailable after one retry, enter `WAIT_USER` and do not infer identity from provider, profile, title, memory, or enum.
If a second reviewer exists or was unambiguously adopted but either `model_diversity_verified` proof is missing or partial, re-resolve both exact model identities once; persist literal `true` on both entries when they differ, archive the second child and fresh-retry on collision, and enter `WAIT_USER` if either identity remains unavailable.
Operational author_provider_resolution and model_diversity_verified fields are excluded from runtime tuples, candidate identity, review-contract identity, review JSON, and offline STATE-checker closure predicates.
明确删除的复杂度只禁止 runtime tuple 的预注册／持久化，
不禁止上述创建／恢复时的 live comparison 与 derived operational provenance。

### 工作流与记录

实现任务采用：PLAN → IMPLEMENT → VALIDATE → REVIEW → ADJUDICATE →（FIX → VALIDATE → RE_REVIEW，最多五轮）→ FINAL_REVIEW → ADJUDICATE → FINAL_VALIDATE → DONE。仅审核任务采用：PLAN → REVIEW → ADJUDICATE → DONE。需要用户决定时记为 WAIT_USER；取消或无法继续时只有在全部 child 已确认归档后才记为 STOP，否则进入 WAIT_USER。

启用 Paseo 时只需维护以下已忽略文件：

- .ai/task/<task_id>/SPEC.md：范围、允许修改文件、验收标准；
- .ai/task/<task_id>/PLAN.md：大型任务的简短步骤；
- .ai/task/<task_id>/BASELINE.patch 或 baseline/：仅在任务需要修改既有脏文件时；
- .ai/task/<task_id>/CODE_DIFF-<phase>-<cycle>-<attempt>.patch：仅 code review phase；
- .ai/task/<task_id>/SCOPE.json：仅在 translation_contextual_v1 冻结前，保存本次离线 anchor preflight 的严格范围；
- .ai/task/<task_id>/CONTEXTUAL-ENVELOPE-<dispatch_id>.json：仅选择 translation_contextual_v1 时；
- .ai/task/<task_id>/STATE.json：当前状态、轮次、审核阶段、角色 ID、transport 和恢复点；
- .ai/reviews/<task_id>/review-NN.json：任务身份、审核阶段、review contract、reviewer role、purpose、dispatch_id、agent_id、candidate_ref、finding 与裁决；STATE 的 `review_records`／`senior_review_records` 新写入为这些 workspace-relative 文件路径的数组。

终态收束使用 `python3 -B tools/ai_state_check.py STATE.json [--target DONE|STOP]`。
它只离线核验 `DONE`／`STOP` 的持久化 closure predicate；`STOP` 只要求无 child 或每个
child 的规范化 lifecycle 为 `archived` 且 `archive_confirmed` 为 literal `true`。
A child counts as archived only when its normalized lifecycle is `archived` and `archive_confirmed` is literal `true`.
`.ai/legacy-cohort-manifest.json` 是 B-prime 采用时的 task-id 边界，只有列出的历史 task 返回信息性
`UNSUPPORTED_LEGACY`，不验证、重写或刻画其既有交付。任何未列入 task（即使字段缺失）都
必须完整通过新契约，不能回退历史兼容路径。manifest 只含 `schema_version` 和按字典序去重的
`unsupported_tasks` 数组。

每个新任务使用独立 task ID；旧的 flat STATE 和 review 记录保持原样。STATE 在阶段转换、contract 完成、agent ID 变化、出现错误或 child 生命周期字段变化时更新；每次 `archive_attempts_started` 递增必须在外部归档调用前立即持久化。除此之外不要求逐动作审计链、全工作树 hash 或 immutable artifact。基础设施错误可重试一次；若创建是否成功不明确，先按 `labels.task_id`、`labels.role` 和需要的 `labels.purpose` 查询；过滤先于基数判定：先排除已记入 `child_dispatches` 的历史 ID，不得按远端 lifecycle 排除未知结果。无匹配可重试一次；唯一匹配且身份正确时先将其完整身份和观测 lifecycle 记入 `child_dispatches`，仅 active 可复用，archived 核验并记录归档确认且不得重试创建，其他 lifecycle 按已记录 agent_id 进入 reconciliation；多个匹配或无法确认时进入 WAIT_USER。

语境 REVIEWER 恢复只允许复用同一候选、同一 dispatch_id、同一 role/purpose 和同一创建尝试的唯一 agent。每次新的派发、重跑或无效输出重试都创建 fresh agent；不得用旧会话部分输出拼接新结果。其他角色需要更换 child 时，也必须保持同 role、同 purpose、同 workspace 和同 lineage，旧未验收输出作废。

### 外发边界

外发权限按角色、purpose 和输入边界授权：

- EXECUTOR：任务 briefing、SPEC 允许的 workspace 内容；
- 普通 REVIEWER：有界代码、工具、文档 diff、SPEC 和必要上下文；
- SENIOR_REVIEWER：同一 SPEC、diff 及 scope audit 所需的当轮 finding；
- SCOUT：组件范围、公开源码根和机制问题；
- translation_contextual_v1 REVIEWER：冻结的有界译文语境 bundle，以及其中明确引用的译文和公开源码。

bundle 不得包含先前 finding、裁决或建议修复。改变外发内容范围、目的或读取边界仍须用户授权；执行载体选择不构成额外的授权轴。质量 evaluator 的运行身份、预注册、campaign ledger 和历史 assessment 由独立质量契约管理，不因本编排契约改变。

## 汉化工具入口

- 自动化统一使用 `python3 -B tools/i18n <command>`；首次运行执行 `doctor`，译文修改后执行 `lint`。工具与报告只在任务允许的边界内工作，派生文件写入已忽略的 `.artifacts/i18n/`。
- 翻译 proposal 必须经 `tools/i18n proposal --strict` 校验；审核、源码侦察和计划审查只走 Paseo 角色路由，具体权限与外发边界见上文。
- Lua 仅按 Lua 5.1／LuaJIT 运行；使用 manifest、`TOME_LUAJIT` 和 `TOME_LUAROCKS_ROOT`，直接 Lua 调用也必须在同一次调用中配置搜索路径。LPeg 固定为已验证的 0.10.2；不得退回新版 Lua。
- 审核、修复和门禁操作步骤见 [`docs/agent-workflow.md`](docs/agent-workflow.md)；Lua、提取器兼容设置、依赖命令与工具／manifest 说明见 [`i18n/README.md`](i18n/README.md)。

## DLC 源码输入（GPL v3 公开）

- ToME4 与三个官方 DLC 为 GPL v3（or later）公开源码，可以直接读取、分析和提取；manifest 固定 engine／extractor 的 commit、组件映射及 DLC 提取基线的快照哈希／条目数，但不固定 DLC 源码仓库、源码 commit 或 1.7.4 源码版本；不在文档中固定本机路径。
- 分发译文／addon 时保留版权声明、使用 GPL v3 兼容许可并提供对应源码。公开源码可由 Paseo 的 REVIEWER／EXECUTOR／SCOUT 及主代理按外发边界只读核验。

## 文档权威顺序

仓库级授权与不变量以本文件为准；激活时的 Paseo 契约、适用的
[`docs/agent-workflow.md`](docs/agent-workflow.md) 和 [`i18n/README.md`](i18n/README.md)
依次承载下层约束与操作细节，均不得放宽上层规则。任何下层文档与本文件冲突时，
以上位规则为准。

## 门禁触发

- 译文每批执行 `docs/agent-workflow.md` 的五步门禁；术语批次在五步后追加三项术语审计。
- 翻译、术语或工具行为变更收束时运行 `tools/ci-gates.sh`；只有 SPEC 证明不影响 addon 输出或构建时才可 `--skip-build`。
- 纯文档任务只运行相关文档／契约检查和 `git diff --check`。完整操作、源码优先判定和术语维护步骤见 [`docs/agent-workflow.md`](docs/agent-workflow.md)。

## 校对判定依据

- 当翻译、术语、审核意见或英文表面含义对游戏机制的描述存在分歧时，对 manifest 已固定 commit 的源码以其实际行为为最终判定依据；对来源未固定的 DLC，必须以实际可核验的公开源码证据为准并标明来源未固定。现有译文、术语库和模型 finding 都不能覆盖源码事实。
- 核验机制时应记录对应组件、公开源码路径、适用的固定 commit（若有）和关键调用或数据定义；若来源或 commit 未固定，必须明确记录并标为待确认，据此确认、部分确认、撤销或修订审核结论。当前工作树与固定 commit 不一致时，默认以版本清单固定的 commit 为准，除非用户明确指定其他目标版本。
- 公开游戏与三个官方 DLC 源码可以直接核验；未公开组件只使用用户授权的证据。证据不足时标为待确认。

## 术语库工作流

- 开始翻译或审校前，先阅读 `TERMINOLOGY.md` 和 `terminology/`。
- 术语/专名疑点只能在审核 observation 产生后按 claim 核验与裁决；不得用术语库覆盖源码事实。
- 新增或修改高复用术语时，先更新 `terminology/`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
