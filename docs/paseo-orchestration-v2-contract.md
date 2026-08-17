# Paseo 轻量编排 v2 设计

> 状态：设计草案，运行时解耦版。
>
> 契约版本：`paseo-orchestration/2.12-draft`。
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

### 明确删除的复杂度

本版本不要求：

- 为角色指定固定运行时载体、版本、mode 或 thinking 档位；
- 任务开始前的运行时发现、精确元组核验和固定 primary／backup 路由；
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
.ai/task/<task_id>/CONTEXTUAL-ENVELOPE-<dispatch_id>.json
.ai/task/<task_id>/STATE.json
.ai/reviews/<task_id>/review-NN.json
```

仅在任务需要时创建 BASELINE、baseline 和 contextual envelope。已有 legacy flat 文件保持
原路径和内容；新任务不得复用已有 task ID，也不得覆盖其他任务记录。

### SPEC 与 PLAN

SPEC 必须写明任务模式、范围、允许修改文件、禁止扩展项和可执行验收标准。PLAN 只记录
主要步骤和依赖，不维护逐动作日志。

### 最小 STATE

```json
{
  "schema_version": 2,
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
  "senior_reviewer": {
    "role": "senior-reviewer",
    "purpose": null,
    "agent_id": null
  },
  "child_dispatches": [],
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": {},
  "senior_review_records": [],
  "wait": null,
  "last_error": null,
  "updated_at": "..."
}
```

`contextual_reviewer` 和 `scout` 是条件字段：只有任务实际选择相应角色／purpose 时
才写入。语境派发后，`candidate_identity`、`dispatch_id`、`input_path` 和
`agent_id` 必须非空并与当前冻结候选一致；SCOUT 不产生审核记录。

STATE 在阶段变化、contract 完成、agent ID 变化、出现错误或 child 生命周期字段变化时
更新；每次 `archive_attempts_started` 递增必须在外部归档调用前立即持久化。
`orchestrator_agent_id` 在任务内不得改变。角色字段是当前契约身份；历史运行时元数据
不参与新任务的有效性判断。

`child_dispatches` 是紧凑的 dispatch 历史；每次创建 child 追加一条记录，记录保留至任务
结束且不得删除。每条记录保存 `role`、`purpose`、`agent_id`、`status`、
`archive_confirmed` 和 `archive_attempts_started`；语境 REVIEWER 的记录还必须保存不可变的
`candidate_identity`、`dispatch_id` 和 `input_path`。child 创建成功后 `agent_id` 必须
非空，且这些身份字段创建后不可修改。`status`、`archive_confirmed`、
`archive_attempts_started`、`last_error` 和 `archived_at` 是生命周期字段，按传输结果在
保留的原记录上更新。`archive_attempts_started` 初始为 0，最大为 2（首次尝试加一次自动
重试）。`status` 至少区分 `active`、`stopping`、`terminal`、
`archive_pending` 和 `archived`，而 `archive_confirmed` 只有在传输返回可核验的归档状态
后才可为 true。当前 active dispatch 是角色当前字段所指向的、且状态为 `active` 的唯一
记录；只有它可以在恢复时复用。

当前 ORCHESTRATOR 进程必须有非空 `PASEO_AGENT_ID`。每个子 agent 都必须由当前 ORCHESTRATOR 进程直接创建，使用 agent-scoped 的 Paseo 创建
接口或其 CLI 等价操作。创建载荷至少包含 workspace、task／role label 和初始 briefing。
Paseo daemon 必须以 `PASEO_AGENT_ID` 对应的 ORCHESTRATOR 建立 parent lineage，并在状态
面报告 `ParentAgentId` 或等价的 `paseo.parent-agent-id`；不得用 top-level placement 或
其他 agent 创建接口替代。角色和 purpose label 必须与 STATE 一致。

### Review 记录

每份 review 记录必须保存 `task_id`、`review_contract`、`review_phase`、`cycle`、
`reviewer_role`、`purpose`、`agent_id` 和完成状态。语境 review 还必须保存
`candidate_identity`、`dispatch_id` 和 `input_path`。每份 code review
记录还保存派发时的 `candidate_ref`；派发、返回和 contract 完成前的引用必须一致。

记录只保存 finding、证据、裁决和结果，不要求复制完整 prompt、运行时选择或构造 lineage
manifest。已完成的历史记录不重写。

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
   先排除已经存在于 `child_dispatches` 的历史 ID，但不得按远端 lifecycle status 排除尚未
   记录的结果。无匹配可重试创建一次；唯一匹配且身份全部正确时，无论其状态如何，先把
   完整不可变身份、观测到的 status 和初始生命周期字段追加到 `child_dispatches`。status 为
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
`last_error`，保持 `status=stopping`，进入 `WAIT_USER`，不把它当作已取消。若传输支持
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

---

## 十三、修订记录

| 版本 | 状态 | 内容 |
| --- | --- | --- |
| `2.12-draft` | 设计草案 | 增加完成即归档、保留 dispatch 记录、不可变身份字段、持久化 `archive_attempts_started` 预算与原地更新生命周期字段；明确 `archive_pending` 在外部归档状态解决并确认前必须停留 `WAIT_USER`，拆分创建歧义发现、已知终态 reconciliation 与 active 恢复，明确语境重试保留候选／输入但更换 dispatch／agent，并要求 `DONE`／`STOP` 前完成全部归档。 |
