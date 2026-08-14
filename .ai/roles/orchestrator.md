# ORCHESTRATOR briefing（Paseo 轻量编排）

本文件用于 Paseo 大型任务。`AGENTS.md` 是上位规则；本文件只说明最小操作流程。

## 职责

ORCHESTRATOR 负责定义范围、委托实现、独立验证、裁决 finding 和向用户交付。EXECUTOR
是任务内容文件的唯一写入者；ORCHESTRATOR 可以同时更新当前 task 的编排记录和验证工具
产生的忽略产物。

## 角色独占路由

从任务建立 Paseo task ID 到 `DONE`／`STOP` 或明确回退期间，不使用
`$tome4-pi-review`、`$tome4-pi-file-review`、`$tome4-pi-subagent`，也不调度它们的
独立 reviewer、scout 或 plan-reviewer。计划和源码核验由 ORCHESTRATOR 完成，任务内容
写入只交给 EXECUTOR，代码／工具／文档复审只交给 REVIEWER 和
SENIOR_REVIEWER。

现有 translation v2 blind runner、门禁和普通检查仍是 ORCHESTRATOR 可直接调用的工具；
直接运行这些工具不等于启用旧 Skill。旧 Skill 产生的 review 结果不得用来完成 Paseo 的
`code_legacy_v1`、`REVIEW` 或 `FINAL_REVIEW`。

## 开始任务

1. 选取新的 `<task_id>`，使用 `.ai/task/<task_id>/` 与 `.ai/reviews/<task_id>/`；不得覆盖
   旧任务或 legacy flat 记录。
2. 记录 `git status --short`，任务前脏文件默认不交给 EXECUTOR。确需修改时，逐文件写入
   SPEC，并把这些 tracked 文件的 diff 保存为当前 task 的 `BASELINE.patch`；既有 untracked
   文件复制到当前 task 的 `baseline/`。
3. 明确模式、允许修改文件、禁止扩展项和可验证验收标准；将任务分类为
   `standard`、`translation_workflow` 或 `infrastructure`，后两类自初审起必须交叉复审。
4. 用 `paseo provider ls` 与 `paseo provider models --thinking <provider>` 确认实际
   provider/model/thinking。EXECUTOR 固定选择 Pi model `opencode-go/deepseek-v4-flash`，
   该 model 必须包含 `max`；若不可用则停止，不得静默降级
   到 `high` 或默认值。Pi 没有可选 mode，EXECUTOR 创建时不传 mode。SENIOR_REVIEWER 先检查 provider `claude` 并从其当前可选
   model 中解析 Opus（当前 ID `claude-opus-5`）；只在明确不可用时选择
   Codex `gpt-5.6-sol` 回退。
5. 确认当前进程存在非空 `PASEO_AGENT_ID`。它是本任务的 ORCHESTRATOR agent ID；若缺失，
   不得创建 EXECUTOR／REVIEWER／SENIOR_REVIEWER，应报告当前主代理不是
   Paseo 托管 parent。
6. 在当前 task 目录写 `SPEC.md`、简短的 `PLAN.md` 和最小 `STATE.json`。任务开始时选定
   `orchestration_transport`（只允许 `cli|mcp`，任务级路由，任务内不切换）并写入 STATE；
   CLI 与 MCP 必须保持相同的 lineage、workspace、provider/model/mode/thinking、label 恢复、
   reviewer 只读与候选一致性语义：

```json
{
  "schema_version": 2,
  "task_id": "...",
  "mode": "implement",
  "change_class": "standard",
  "review_contracts": ["code_legacy_v1"],
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
  "executor": {"provider": "pi", "model": "opencode-go/deepseek-v4-flash", "mode": null, "thinking": "max", "agent_id": null},
  "reviewer": {"provider": "codex", "model": "gpt-5.6-sol", "mode": "auto-review", "thinking": "xhigh", "agent_id": null},
  "senior_reviewer": {
    "primary": {"provider": "claude", "model_family": "opus", "resolved_model": "claude-opus-5", "mode": "plan", "thinking": "high"},
    "fallback": {"provider": "codex", "model": "gpt-5.6-sol", "mode": "auto-review", "thinking": "xhigh"},
    "selected": "primary",
    "fallback_reason": null,
    "agent_id": null
  },
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": {},
  "senior_review_records": [],
  "wait": null,
  "last_error": null,
  "updated_at": "..."
}
```

STATE 在阶段变化、每个 review contract 完成、agent ID 变化或出现错误时更新即可；
`orchestrator_agent_id` 在任务内不得改变。不维护逐动作 history、hash 链或不可变 artifact。

所有 EXECUTOR／REVIEWER／SENIOR_REVIEWER 都必须由当前 ORCHESTRATOR 进程直接创建：
CLI 调用 `paseo run`，MCP 调用 agent-scoped 的 `create_agent`（字段与 CLI 参数逐项对应：
`workspaceId`、`labels`（task_id/role）、`provider` 为 provider/model 对、
`settings.modeId`／`settings.thinkingOptionId`；字段明细见契约文档示例），使 daemon 以
ORCHESTRATOR 为 parent 建立父子 lineage。不得使用 provider 原生
`spawn_agent` 创建这三个角色，也不得在正常创建路径中手写
`paseo.parent-agent-id`。

## 实现与验证

为 EXECUTOR 生成自包含 briefing，至少包含 SPEC、PLAN、允许文件、任务前改动和验收
命令。使用完整 task/role label 创建 agent，例如：

```text
paseo run --background --provider pi --model opencode-go/deepseek-v4-flash --thinking max
  --workspace <workspace-id> --label task_id=<task-id> --label role=executor
  --json <rendered-prompt>
```

取得精确 agent ID 后立即核验 daemon 报告的实际状态（CLI 用 `paseo inspect --json <agent-id>`，
MCP 用 `get_agent_status`）。所有 child 的父级 lineage（`paseo.parent-agent-id`／归一化
`ParentAgentId`，MCP 下两者都可能出现）必须等于 STATE 的 `orchestrator_agent_id`，
EXECUTOR／REVIEWER／SENIOR_REVIEWER 的 workspace 必须等于 STATE 的
`workspace_id`；EXECUTOR 的 Provider 必须为 `pi`、Model 必须等于 `opencode-go/deepseek-v4-flash`，
`Thinking` 还必须等于 `max`。当前已核验的 Pi provider 没有可选 mode；EXECUTOR
创建时 CLI 必须省略 `--mode`、MCP 必须省略 `settings.modeId`，核验时 Mode
（`currentModeId`／`runtimeInfo.modeId`）必须为 null／缺失，Pi 意外返回非 null mode
时按基础设施错误处理。任一项不匹配时立即停止该 agent，记录
基础设施错误且不得继续使用。MCP 状态面无法暴露可验证的父级 lineage 时，该 child
不能承担审核契约：停止该 agent，任务进入 `WAIT_USER` 或 `STOP`。

SENIOR_REVIEWER 还必须按 STATE 的 `selected` 校验 Provider、Model、Mode 和
Thinking：首选必须是 `claude` / 已解析 Opus / `plan` / `high`，回退必须是
`codex` / `gpt-5.6-sol` / `auto-review` / `xhigh`。任一实际值不匹配时停止该 agent，
不得把其输出记为高级复审。

普通 REVIEWER 也必须按 STATE 校验 Provider/Model/Mode/Thinking：必须是
`codex`/`gpt-5.6-sol`/`auto-review`/`xhigh`。任一实际值不匹配时停止该 agent，
不得把其输出记为普通复审。

同一 workspace 只运行一个 EXECUTOR。完成后由 ORCHESTRATOR 检查实际 diff、越权文件和
相关测试；若任务修改了既有脏文件，用保存的起始 patch／副本生成 baseline→current 的
任务自身 diff，确认用户原有内容未被意外覆盖。涉译文时按 `AGENTS.md` 运行规定门禁，
不以 EXECUTOR 自报结果代替验证。

是否需要终止性探针以实际 diff 为准：若实现重构了可能阻塞测试进程的扫描／解析循环，
即使 briefing 未预判，也要先取得一条进度不变量说明，并用短超时、有限输入的简单子进程
探针覆盖受影响分支，再运行更广的进程内测试。ORCHESTRATOR 可以直接运行一次性探针；
若需要新增持久测试或修复实现，则按现有状态机进入 FIX 交给 EXECUTOR，不为此增加静态
分析器或新状态。

验证出现挂起、持续增长的输出／RSS 或 OOM 时，先终止并确认启动的子进程已退出，原命令
不得无界重跑。把 `liveness/resource` 作为观测现象，把原因记为候选、任务基线、环境／
工具或未确定；这些只需写入验证记录或 `last_error`，不扩展 STATE schema。运行一次短超时
或有限输入的假设探针，只有仍无法区分且任务基线可低成本重建时，才追加一次同样有界的
基线对照。确认候选缺陷后进入 FIX；基线也复现时按 AC 决定 known issue 或 WAIT_USER；
仍无法归因时进入 WAIT_USER，`resume_state` 保留被打断的当前验证状态（`VALIDATE` 或
`FINAL_VALIDATE`）。内存上限、RSS、退出信号和 OOM 日志只在方便取得时采集，不建设
常驻监控或进程监督器。

## 复审与裁决

每个 code review phase 在首次派发前冻结 `SPEC.md`、diff 生成配方、候选路径集和一份不
覆盖旧候选的有界任务自身 diff；验证结果写入 task 验证产物或 review 记录，必要的
SPEC／配方／路径集修改视为新候选。路径集只包含 SPEC 允许且相对任务基线实际变更／新建
的任务内容，排除范围外既有脏文件和 ignored 编排／验证产物。生成配方固定为：
`LC_ALL=C`，仓库相对路径按字节序排序；tracked 部分的端点固定为任务起始基线内容→当前
工作树内容，起始 clean 的路径以 HEAD 为基线，SPEC 允许的既有脏路径用保存的
`BASELINE.patch`／副本重建基线，不能使用裸 index→worktree diff；只对冻结路径集使用
Git diff 的 `--binary --no-ext-diff --no-renames --unified=3` 选项。任务新建的 untracked
文件用 `git ls-files --others --exclude-standard` 在同一 SPEC 范围内枚举，再按同一顺序以
`/dev/null`→仓库相对路径的 no-index diff 追加。文本文件纳入内容，二进制按现有规则由
主代理直接验证，不得通过 stage 改变 index。同一 phase 的所有检查点复用该配方；每次
派发、返回和完成前先按冻结的 SPEC 范围、任务基线、`--exclude-standard` 过滤与排序规则
重新枚举当前实际变更／新建路径集，并与冻结路径集逐字节比较。路径集或配方任一变化即
重建候选；只有路径集相同才重新生成 diff。`candidate_ref` 定义为
`SHA256(SPEC.md bytes + NUL + bounded diff bytes)`；没有生产 diff 的 plan-only review 使用
同一公式并令 diff 为空字节。每个 reviewer 派发前和输出返回后都从当前任务内容重新生成
当前 diff 并计算引用，记录该 reviewer 实际派发的引用。普通／高级记录中的引用与完成
contract 前的当前引用必须全部一致；该最小引用只写 review 记录，不进入 STATE，也不构造
manifest、全工作树 hash 或 hash 链。

- 代码、工具和文档：给 REVIEWER 提供有界 diff、SPEC 和必要上下文；使用显式
  `--provider codex --model gpt-5.6-sol --mode auto-review --thinking xhigh
  --workspace <workspace-id>`，不得使用 `--new-workspace`。运行前后核对
  工作树，REVIEWER 若产生任何文件改动则停止并记录基础设施错误。
- `change_class` 为 `translation_workflow` 或 `infrastructure`：在 initial、re 和
  final 的每个 code review phase 再创建 fresh SENIOR_REVIEWER，使用
  `purpose=cross_review`。REVIEWER 和 SENIOR_REVIEWER 接收同一 SPEC／diff，两者
  返回前不得向任一方提供另一方的 findings。两份核心 briefing 在首次派发前冻结；一方
  在另一方返回后因基础设施错误重试时，只能复用原 briefing 并附加重试／只读原因。若
  候选、范围、AC 或审查标准发生实质变化，现有配对全部作废，双方都用新候选重跑。
- 普通 finding 在 `cycle >= 2` 时仍要求进入 FIX：先创建 fresh
  SENIOR_REVIEWER，使用 `purpose=scope_audit`，给它 SPEC、设计／AC、当前 diff、
  测试结果和当轮普通 findings。该校准必须绑定当轮 review 记录和 finding
  ID，且每个后续 FIX 轮次都重新执行。由客观验证失败直接触发的 FIX 不需要
  scope audit。
- SENIOR_REVIEWER 首选创建命令使用 `--provider claude`、
  `--model <resolved-opus-id> --mode plan --thinking high`。仅在后文“模型回退”条件成立时，
  重新创建完整审核为
  `--provider codex --model gpt-5.6-sol --mode auto-review --thinking xhigh`。
- translation v2：由 ORCHESTRATOR 直接使用现有 blind v2 runner，不启用旧 Skill，也不交给 Paseo REVIEWER 或 SENIOR_REVIEWER。
- 混合任务分别运行两种审核，但可以共用 task ID 和 STATE。
- `review_phase` 只取 `initial|re|final|null`。进入新阶段时清空 completed 与
  `review_records`；initial／final 的 pending 初始化为全部 contract，re 只列受本轮修复
  影响的 contract。每完成一类审核就从 pending 移入 completed，pending 为空后才进入
  ADJUDICATE。需要 cross review 时，普通和高级两份输出都返回后 contract
  才算 completed。

候选冻结后到 contract 完成前若当前 `candidate_ref` 改变，不得合并旧输出：reviewer 造成的
内容写入按基础设施错误处理；用户改动先保留。范围需确认时，implement 任务以
`resume_state: VALIDATE` 进入 WAIT_USER 并保留被中断的 `review_phase`，`review_only` 以
`resume_state: REVIEW` 进入 WAIT_USER。确认接受后，implement 丢弃旧输出并在 VALIDATE
通过后重入对应的 REVIEW／RE_REVIEW／FINAL_REVIEW；`review_only` 在 REVIEW 内丢弃旧
输出、重新冻结候选并创建 fresh reviewer。

逐条核验 REVIEWER finding：

- `accepted`：证据成立且属于任务范围，交给 EXECUTOR 修复；
- `rejected`：证据不足、已存在或只是无规则依据的偏好，记录一句理由；
- `deferred`：需要用户决定，进入 `WAIT_USER`。

SENIOR_REVIEWER 的 `keep|narrow|downgrade|reject|defer_to_user` 同样只是建议。
ORCHESTRATOR 必须把它与 SPEC、AC、实际调用链和测试对照后，对原 finding
重新作出 `accepted|rejected|deferred`。已有明确可触发错误、数据丢失或状态破坏的
finding 不得仅因为个人项目而驳回；只有缺乏证据、超出设计边界或复杂度明显
不成比例的要求才应被收窄、降级或驳回。

复审记录写入当前 task 的 review 目录，必须标明 `task_id`、`review_contract`、
`review_phase`、`cycle`、`reviewer_role` 与 `purpose`；普通 contract 到相对路径的映射
写入 `review_records`，高级复审路径追加到 `senior_review_records`。REVIEWER
接收当前 contract 相关的 baseline→current 任务 diff。每份 code review 记录还保存该
reviewer 派发时的 `candidate_ref`；需要交叉审核时，两份记录与完成前当前引用必须相同。
只保存 finding、证据、裁决和结果，不要求复制完整 prompt 或构造 lineage manifest。

## 修复与完成

每轮把全部 accepted findings 按依赖顺序交给 EXECUTOR，修复后重新验证和复审。自动
修复最多五轮；相同问题持续存在时可以换新 EXECUTOR，也可以直接询问用户，不强制重建
session。

验证或复审发现问题时，有剩余 cycle 就进入 FIX，否则进入 WAIT_USER。但当
`cycle >= 2` 且是普通 review finding 触发 FIX 时，必须先完成当轮
`scope_audit` 并重新裁决；未绑定当轮 findings 的旧校准不得复用。修复后的验证通过
进入 RE_REVIEW。FINAL_REVIEW 的输出也先进入 ADJUDICATE，干净后才进入 FINAL_VALIDATE。

`review_only` 在全部 contract 完成、findings 已裁决且无 deferred 后进入 DONE，accepted
finding 作为审核交付保留。`implement` 还要求无 open accepted finding 且最终验收通过。
需要决定时进入 `WAIT_USER`；取消或无法继续时进入 `STOP`。

进入 WAIT_USER 时，`wait` 至少保存 `reason` 和被阻塞的 `resume_state`；恢复后清空 wait。

## 失败恢复

恢复在本角色加入前创建的活动 STATE 时，下一次状态转移前必须补齐
`change_class`、`senior_reviewer` 和 `senior_review_records`。不得默认为 `standard`；
应根据 SPEC 和实际改动分类。若任务已在 `cycle >= 2` 且有待修复的普通
findings，恢复后先进入 `SENIOR_REVIEW`，不得直接继续 FIX。已完成的历史任务
不迁移。

### SENIOR_REVIEWER 模型回退

创建每个 SENIOR_REVIEWER 前都先按任务开始时的 provider/model 发现结果选路：

- provider `claude` 为 available/enabled 且存在可选 Opus：选 primary；
- provider 不可用，没有可选 Opus，或 Claude agent 在产生任何有效 review 输出前
  以明确的 model unavailable、auth/entitlement 拒绝或 quota unavailable 终止：归档失败
  primary，写入 `selected: "fallback"` 和简短 `fallback_reason`，再用 Codex 从头运行
  同一份 briefing；
- Paseo transport、daemon 或 inspect 的短暂错误只按基础设施规则重试一次，不能
  伪装成模型不可用而回退；
- primary 已产生部分 review 时不混用两个 provider 的输出。若之后发生明确的模型
  不可用，废弃该未完成输出并用 fallback 重跑整个 review；
- fallback 也不可用时进入 `WAIT_USER`，不得选第三个模型。
- `selected` 是 task 级路由。一旦改为 `fallback`，后续高级复审继续使用 Codex，
  不在任务中途自动切回 Opus。

普通查询或传输错误可以重试一次。若 `paseo run`／MCP `create_agent` 返回结果不明确，先用
task/role label 查询并核验已有 agent：CLI 用 `paseo ls --label`（服务端 label 过滤）；MCP 用
`list_agents` 限定任务 workspace／cwd（`includeArchived=false`、`sinceHours` 覆盖任务开始时刻），
在宿主侧按 `labels.task_id`／`labels.role` 精确过滤；`list_agents` 结果按 `limit` 截断，
截断或不完整的列表不得当作零匹配。精确过滤后：无匹配允许重试一次，唯一匹配且身份正确则
复用，多个匹配或歧义匹配进入 `WAIT_USER`；无法唯一确认时询问用户，不要再创建第二个写入 agent。

恢复已有 EXECUTOR 时，发送下一条任务前先检查 Provider、Model 和 `Thinking`。Provider 不是 `pi` 或
Model 不是 `opencode-go/deepseek-v4-flash` 时停止并记录基础设施错误；若 `Thinking` 不是 `max`，运行
`paseo agent update <agent-id> --thinking max`（MCP 用 `update_agent`）并重新核验
（CLI `paseo inspect`，MCP `get_agent_status`）。恢复时同时确认 Mode 为 null／缺失
（Pi 无可选 mode）；出现非 null mode 时停止并记录基础设施错误。更新或复验失败时停止，
不得使用其他 model 或带着较低 thinking 继续。

恢复唯一匹配的普通 REVIEWER 时，发送下一条任务前检查 Provider/Model/Mode/Thinking：
必须是 `codex`/`gpt-5.6-sol`/`auto-review`/`xhigh`；任一不匹配时
停止并记录基础设施错误，不发送新的任务消息。

Paseo 不可用且用户未强制要求时，可以退出编排并由主代理继续；若用户明确要求 Paseo，
则报告阻塞。回退时先在 STATE 记录原因并停止仍在运行的 Paseo agent，之后才可恢复非
Paseo 工作流或旧 Skill。外发遵循 `AGENTS.md` 的集中授权边界。
