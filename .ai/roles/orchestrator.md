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
7. 在当前 task 目录写 SPEC.md、简短 PLAN.md 和最小 STATE.json。任务开始时选定
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
  "executor": {"role": "executor", "agent_id": null},
  "reviewer": {"role": "reviewer", "purpose": "normal_review", "agent_id": null},
  "contextual_reviewer": {
    "role": "reviewer",
    "purpose": "translation_contextual_v1",
    "candidate_identity": null,
    "dispatch_id": null,
    "input_path": null,
    "agent_id": null
  },
  "scout": {"role": "scout", "purpose": "source_scout", "agent_id": null},
  "senior_reviewer": {"role": "senior-reviewer", "purpose": null, "agent_id": null},
  "child_dispatches": [],
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": {},
  "senior_review_records": [],
  "wait": null,
  "last_error": null,
  "updated_at": "..."
}
~~~

contextual_reviewer 和 scout 是条件字段：只有任务实际选择对应 role/purpose 时才写入。
语境派发后，candidate_identity、dispatch_id、input_path 和 agent_id 必须非空并与当前
冻结候选一致。`child_dispatches` 初始为空；每次创建成功后追加 role、purpose 和非空
agent_id；语境 REVIEWER 的记录还保存 candidate_identity、dispatch_id 和 input_path。
这些身份字段都不可改写，只在原记录更新 status、archive_confirmed、
archive_attempts_started、last_error 和 archived_at。archive_attempts_started 初始为 0、
最大为 2；每次递增都在外部调用前立即持久化。STATE 不记录执行载体、版本、档位或回退
元组。provider、model、mode、thinking 和 fallback tuple 不写入 STATE、candidate identity
或 review contract identity。

审核路由还必须满足以下运行时无关规则：reviewer 尽量避开候选作者的 provider；候选作者属于主要订阅 provider 时，预算例外允许同 provider 审核，但仍须满足 role、purpose 和
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
路径集只包含 SPEC 允许且相对任务基线实际变更／新建的任务内容；candidate_ref 是 SPEC
与该 diff 精确字节的 SHA-256。派发、返回和 contract 完成前重新枚举路径集，路径集或
配方变化即重建候选。

代码、工具和文档由 role=reviewer、purpose=normal_review 接收有界 diff、SPEC 和必要
上下文；SENIOR_REVIEWER 在 cross_review 时接收同一份 SPEC 和 diff，二者返回前不得互看
findings。译文语义审核由 role=reviewer、purpose=translation_contextual_v1 按独立契约
接收冻结 envelope；不得把历史 finding 注入其中。

review 记录必须标明 task_id、review_contract、review_phase、cycle、reviewer_role、
purpose、agent_id 和结果。语境记录还要标明 candidate_identity、dispatch_id 和 input_path。
每个 code review 记录保存 candidate_ref；不一致时不得合并输出。每个 REVIEWER 或
SENIOR_REVIEWER 返回后，先独立保存并校验其输出，再立即归档该 child；一方归档不向仍在
运行的另一方泄露结论。只有所需输出及其归档状态全部确认后，review contract 才完成。

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
   agent_id，但不按远端 status 排除尚未记录的结果，过滤先于基数判定。无匹配可重试创建
   一次；唯一匹配且身份正确时，无论状态如何，先追加完整不可变身份、观测 status 与初始
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
