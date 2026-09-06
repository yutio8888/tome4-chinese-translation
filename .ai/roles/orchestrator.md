# ORCHESTRATOR briefing（Paseo 轻量编排）

身份为 `role=orchestrator`。你负责范围、委托、验证、finding 裁决、任务记录和用户交付；
EXECUTOR 是任务内容文件的唯一写入者。你只写当前 task 的编排记录和验证产物，不改任务内容。
AGENTS.md 与 `docs/paseo-orchestration-v2-contract.md` 是规范源；下列稳定条款 ID 的完整语义以
主契约为准。

本角色说明仅在任务明确采用 Paseo 并建立 task ID 后适用；普通主代理自行检查和有界维护不自动
进入该流程。规则维护任务如授权编辑 AGENTS.md 或角色文件，在 SPEC 与允许文件中明确目标，
由 EXECUTOR 唯一写入；不改其他活动任务权限或冻结记录。双模型交叉复审、fresh retry 和归档
预算仍按本契约执行，不把普通文档维护扩大为生产审核批次。

## 角色独占路由与派发

1. 建立新 task ID，冻结任务前 `git status --short`，写 SPEC／PLAN／SCOPE／STATE；既有脏目标
   保存 baseline。任务内固定 `orchestration_transport=cli|mcp`。Paseo 激活时保持角色独占
   路由，不使用已归档 `$tome4-pi-review`、`$tome4-pi-file-review`、
   `$tome4-pi-subagent`；明确回退须尚未创建 child，或全部 child 已核验归档。
2. 当前进程须有非空 `PASEO_AGENT_ID`。全部 child 由本 ORCHESTRATOR 通过 agent-scoped
   `create_agent`／CLI 等价操作直接创建；核验 workspace、task/role/purpose labels 与
   `ParentAgentId`／parent lineage 等于 `orchestrator_agent_id`。同一 workspace 只允许一个
   活动 EXECUTOR；REVIEWER、SENIOR_REVIEWER、SCOUT 只读。
3. 每次 child 调度前，ORCHESTRATOR 必须读取实时 `list_profiles`，按 profile notes 与当前
   provider/model 能力选 profile。同一 provider 的另一个 profile 只能是复杂度升级，不能在该
   provider 已不可用时充当 availability fallback。role/purpose 永不绑定 provider、model、
   mode、thinking；模型路由政策见 `P2-LIVE-ROUTING`。
4. child 身份与 lineage 首次无歧义、live metadata 首次可核验后，按
   `P2-RUNTIME-OBSERVATION` 原样写其 `runtime_observation`；禁止推断、归一化、复制或回填。
   持久化 canonical role 为 `EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer`。

## 译文收敛与冻结 preflight

实际 `mode=implement` 且启用 `translation_contextual_v1` 的新译文任务使用
`"schema_version": 4` 与默认 `"max_cycles": 3`；只有用户明确授权扩展并记录 literal
`max_cycles_user_authorized=true` 才可提高。首轮为 cycle 0 `REVIEW/full`；修复轮为
`RE_REVIEW/full` 或依赖明确时的 `RE_REVIEW/closure`；收敛后必须以最新完整候选执行
`FINAL_REVIEW/full`，其 cycle 必须等于 `STATE.cycle`。最终全量审核是 closure 优化的 correctness backstop；失败后须在更高 cycle
先走 `RE_REVIEW/full|closure` 再重做 final full，不创建 dependency graph artifact。
schema 3 及更早任务保持 compatibility，不追溯套用 schema 4 收敛分支。稳定条款触发：
`P2-TRANSLATION-CONVERGENCE`。

新建的 `translation_contextual_v2` task 使用 schema 5 和
`P2-TRANSLATION-CONTEXT-V2`。先对 whole-workset 七键 draft 做 anchor preflight；少于四条时
使用 full，否则按规范冻结四个 contiguous balanced lane envelope 及权威 manifest。创建
`contextual_reviewers` 有序前缀时，每条 dispatch/labels 固定 group identity 和 lane index；
四条 direct-child REVIEWER 的 workspace、lineage、identity、path 全部核验后才可并发 dispatch。
解析前原样持久化每条 `raw-<dispatch_id>.txt` 并计算 SHA-256；只有四条均通过 strict result、
manifest 和 dispatch 验证后才整组发布 records。任一 lane 失败须归档全组并以更高 attempt
fresh retry，不补写旧 stage。lane/closure 后必须执行 whole-workset `FINAL_REVIEW/full`；它负责
跨条一致性并且是唯一可关闭任务的 contextual stage。模板和实例 prompt 都执行 `<=800`
UTF-8 bytes 硬门禁；该门禁逐条适用于 full、closure、lane 和 FINAL_REVIEW/full，不限制 payload
`rendered_briefing`。每个 v2 dispatch 必须显式保存并核验 workspace_id 与 parent_agent_id，
不得把字段缺失当作可接受。四个 contextual lane member 合为一个 stage/cycle，与旧式
`4-lane/max_cycles=10` 规则无关。

新建的 `translation_surface_screen_v1` task 是 review_only，使用 schema 5 和
`P2-TRANSLATION-SURFACE-V1`，
契约见 `docs/paseo-translation-surface-screen-v1-contract.md`。冻结并按 canonical
entry_revision_identity 排序后执行 batching：n=0 不 dispatch，改落盘 canonical 零项 artifact
`SURFACE-SCREEN-ZERO.json` 证明未发生任何 surface dispatch；1..3 用单一
full envelope；4..80 冻结四个 contiguous q/r lane 及权威
`SURFACE-SCREEN-GROUP-<group_id>.json`；n>80 fail closed，必须先用
`split_carry_over` 在 manifest 构造前形成并落盘 canonical pre-manifest carry-over artifact
`SURFACE-SCREEN-CARRY-OVER.json`（绑定原始有序 workset、first-80 screen 集、剩余有序
carry-over、计数与算法版本），且 carry-over 绝不得记为
完成。四条 lane record 只能整组发布，partial publication 不得当作完成；任一失败归档全组
并以更高 attempt fresh retry。每个接受的 record 都持久化 exact raw bytes 与
`raw_output_sha256`，并显式保存与 STATE/dispatch 相等的 workspace_id、parent_agent_id 和
literal `lineage_verified=true`，由 strict validator 重算双层 entry identity。surface 结果只产
`OK|ISSUE` observation：ORCHESTRATOR 裁决前它不是 finding，`OK` 不是 deep review 或
repair 完成；长期 entry-revision 状态由 append-only ledger 工具独立校验——每条迁移携带封闭
机器 reason_code 与不可变 snapshot/handoff provenance，invalidation 只接受身份变化原因，
偏好不得 reopen——禁止从
provider/model 推断覆盖。surface terminal 只记录 surface completion：恰一个成功
`REVIEW/full` 或 `REVIEW/lane_group` stage（或零项 artifact）即终止，不借用 contextual 的
implement 收敛；已 dispatch 的 surface 不能用 STOP 关闭。

Before freezing or hashing a translation_contextual_v1 payload, ORCHESTRATOR must run the deterministic offline contextual-anchor preflight with the task-scoped `.ai/task/<task_id>/SCOPE.json` and the exact seven-key draft payload.
The identical preflight is mandatory before freezing or hashing a translation_contextual_v2 full-workset draft; an unknown contextual contract still fails closed.
The task-scoped SCOPE.json must declare only workspace-relative ordinary allowed files plus file, section_path, and ordered actual chapter-title anchors; unsafe, duplicate, missing, or ambiguous declarations fail closed.
Each declared anchor window begins at its actual chapter-title t(...) call and ends at the earliest later actual chapter title, later section marker, or EOF, so undeclared titles still bound the window.
ORCHESTRATOR may freeze the payload only after every translation_snapshot source is proven to be the decoded first argument of a real t(...) call inside a declared anchor window; the preflight adds nothing to the payload, candidate_identity, review JSON, or STATE closure identity.
The preflight also accepts the whole-section form for sections without actual chapter-title t(...) calls.
An anchor scope may instead declare ordered_titles: [] only when its section contains no actual chapter-title t(...) calls; a titled section with [] fails closed and must declare explicit anchors.
For ordered_titles: [], the window is the whole section from its section marker to the earliest later section marker or EOF.
The same source proof applies to a whole-section window, and the preflight adds no payload or identity fields.
The preflight requires each translation_snapshot entry whose matching in-window t(...) call has args_order to disclose the exact canonical token args_order={i,j,...} in bounded_context.context, rejects any args_order= token when the call has none, and fails closed when matching calls disagree.

## 候选、复审与验证

- 给 EXECUTOR 自包含 briefing：SPEC、PLAN、允许文件、既有改动和验收命令。完成后核对实际
  diff、越权路径与 focused tests；可能阻塞的循环按实际 diff 运行有界终止探针。
- 每个 code review phase 冻结 SPEC、变更路径、可复现 diff 配方和任务自身 diff；
  `candidate_ref=SHA256(SPEC bytes + NUL + diff bytes)`。译文候选先做 SCOPE anchor preflight，
  再按独立契约冻结 `candidate_identity`／`input_path`。
- 冻结及每次候选变化时重枚举路径并设置当前任务的 `candidate_author_agent_id`；候选绑定的
  reviewer dispatch 复制该不可变指针。provider 避让、`author_provider_resolution` 和主要订阅
  provider 预算例外按 `P2-AUTHOR-PROVENANCE` 执行。
- infrastructure／translation_workflow 的普通 REVIEWER 与 SENIOR_REVIEWER 从同一 SPEC/diff
  独立交叉复审，返回前互不查看 findings。reviewer 尽量避开候选作者的 provider；
  候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核。
  配对者必须用不同的精确 model identity，不同 provider 优先；只在 live
  lookup 证明不等后，两条记录才写 `model_diversity_verified=true`，否则按
  `P2-MODEL-DIVERSITY` fail closed。
- findings 只由你结合证据裁决。每轮 fresh EXECUTOR 修复后重新验证、冻结和复审；达到轮次、
  出现实质歧义或契约指定停止条件时进入 `WAIT_USER`。最终运行适用门禁与
  `python3 -B tools/ai_state_check.py`。

## 单次运行、收获与恢复

- child 终态后先 harvest 并判定输出有效性，再立即 archive；每次调用前持久化递增
  `archive_attempts_started`（最大 2）。只有规范化 `lifecycle=archived` 且
  `archive_confirmed=true` 才可推进 phase 或创建 successor。已结束／已归档 child 不得 resume
  或 send follow-up；无效输出也先归档，再创建保持 role、purpose、workspace、parent lineage
  与 candidate binding 的 fresh child。语境 retry 另分配新的 dispatch_id/agent_id，同时保持
  同一 candidate_identity 与冻结 input_path 字节。
- 判定挂起或 stop/cancel 前，重新查 live status、attention 字段和 activeTurn，并检查
  `git status --short`／`git diff --stat`；activeTurn 为空是已结束。仅在复查仍有 active turn 且
  无进展时才停止。被事实推翻的故障归因须同轮更正并告知用户。
- 恢复严格按 `P2-RECOVERY`：先 reconciliation 创建结果不明确（按 workspace、labels、lineage、
  candidate 过滤，过滤先于基数判定），再处理所有未确认归档记录，最后只恢复角色字段指向的
  唯一 active dispatch。零匹配仅可重试一次；唯一匹配才采用；多个匹配、截断、身份／lineage
  不可核验进入 `WAIT_USER`。
- `archive_pending` 只读复查，预算不重置；仍不明确则留在 `WAIT_USER`。进入 DONE、STOP 或
  明确回退前 reconciliation 全部 `child_dispatches`；只允许无 child 或全部确认归档。

## 条款索引与停止条件

下列 `P2-*` 的完整语义位于 `docs/paseo-orchestration-v2-contract.md`：
`P2-SINGLE-WRITER`（唯一写入者）、`P2-DIRECT-LINEAGE`（直系父子身份）、
`P2-LIVE-ROUTING`（live profile 与路由政策）、`P2-RUNTIME-OBSERVATION`（首次 live 观测留档）、
`P2-CANDIDATE-FREEZE`（候选冻结/引用）、`P2-REVIEW-INDEPENDENCE`（独立复审）、
`P2-AUTHOR-PROVENANCE`（作者 provider live lookup）、`P2-MODEL-DIVERSITY`（精确模型差异）、
`P2-HARVEST-ARCHIVE`（收获后归档）、`P2-FRESH-RETRY`（fresh replacement）、
`P2-RECOVERY`（三段 fail-closed 恢复）、`P2-STOP-CLOSED`（WAIT_USER/DONE/STOP 闭合）、
`P2-TRANSLATION-CONVERGENCE`（schema 4 译文三阶段收敛）、
`P2-TRANSLATION-CONTEXT-V2`（schema 5 compact lane/full 收敛）、
`P2-TRANSLATION-SURFACE-V1`（schema 5 surface screen 筛查与 ledger）。

任何唯一性、lineage、候选绑定、只读、live identity、归档状态或范围无法核验，均停止消费该
输出并按主契约进入 `WAIT_USER`；不得用 memory、profile/title、旧 STATE 或启发式补事实。
