# ORCHESTRATOR briefing（Paseo 轻量编排）

本文件用于 Paseo 大型任务。`AGENTS.md` 是上位规则；本文件只说明最小操作流程。

## 职责

ORCHESTRATOR 负责定义范围、委托实现、独立验证、裁决 finding 和向用户交付。EXECUTOR
是任务内容文件的唯一写入者；ORCHESTRATOR 可以同时更新当前 task 的编排记录和验证工具
产生的忽略产物。

## 开始任务

1. 选取新的 `<task_id>`，使用 `.ai/task/<task_id>/` 与 `.ai/reviews/<task_id>/`；不得覆盖
   旧任务或 legacy flat 记录。
2. 记录 `git status --short`，任务前脏文件默认不交给 EXECUTOR。确需修改时，逐文件写入
   SPEC，并把这些 tracked 文件的 diff 保存为当前 task 的 `BASELINE.patch`；既有 untracked
   文件复制到当前 task 的 `baseline/`。
3. 明确模式、允许修改文件、禁止扩展项和可验证验收标准。
4. 用 `paseo provider ls` 与 `paseo provider models <provider>` 确认实际 provider/model。
5. 在当前 task 目录写 `SPEC.md`、简短的 `PLAN.md` 和最小 `STATE.json`：

```json
{
  "schema_version": 2,
  "task_id": "...",
  "mode": "implement",
  "review_contracts": ["code_legacy_v1"],
  "state": "PLAN",
  "review_phase": null,
  "pending_review_contracts": [],
  "completed_review_contracts": [],
  "cycle": 0,
  "max_cycles": 2,
  "workspace_id": "...",
  "baseline": {"patch": null, "copies_dir": null},
  "executor": {"provider": "pi", "model": "...", "agent_id": null},
  "reviewer": {"provider": "codex", "model": "...", "agent_id": null},
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": {},
  "wait": null,
  "last_error": null,
  "updated_at": "..."
}
```

STATE 在阶段变化、每个 review contract 完成、agent ID 变化或出现错误时更新即可；不
维护逐动作 history、hash 链或不可变 artifact。

## 实现与验证

为 EXECUTOR 生成自包含 briefing，至少包含 SPEC、PLAN、允许文件、任务前改动和验收
命令。使用完整 task/role label 创建 agent，例如：

```text
paseo run --background --provider <provider> --model <model>
  --workspace <workspace-id> --label task_id=<task-id> --label role=executor
  --json <rendered-prompt>
```

同一 workspace 只运行一个 EXECUTOR。完成后由 ORCHESTRATOR 检查实际 diff、越权文件和
相关测试；若任务修改了既有脏文件，用保存的起始 patch／副本生成 baseline→current 的
任务自身 diff，确认用户原有内容未被意外覆盖。涉译文时按 `AGENTS.md` 运行规定门禁，
不以 EXECUTOR 自报结果代替验证。

## 复审与裁决

- 代码、工具和文档：给 REVIEWER 提供有界 diff、SPEC 和必要上下文；使用显式
  `--mode auto-review --new-workspace local`，不要把 main workspace 交给 REVIEWER。
- translation v2：使用现有 blind v2 runner，不交给 Paseo REVIEWER。
- 混合任务分别运行两种审核，但可以共用 task ID 和 STATE。
- `review_phase` 只取 `initial|re|final|null`。进入新阶段时清空 completed 与
  `review_records`；initial／final 的 pending 初始化为全部 contract，re 只列受本轮修复
  影响的 contract。每完成一类审核就从 pending 移入 completed，pending 为空后才进入
  ADJUDICATE。

逐条核验 REVIEWER finding：

- `accepted`：证据成立且属于任务范围，交给 EXECUTOR 修复；
- `rejected`：证据不足、已存在或只是无规则依据的偏好，记录一句理由；
- `deferred`：需要用户决定，进入 `WAIT_USER`。

复审记录写入当前 task 的 review 目录，必须标明 `task_id`、`review_contract`、
`review_phase` 与 `cycle`；当前 contract 到相对路径的映射写入 `review_records`。REVIEWER
接收当前 contract 相关的 baseline→current 任务 diff。只保存 finding、证据、裁决和结果，
不要求复制完整 prompt 或构造 lineage manifest。

## 修复与完成

每轮把全部 accepted findings 按依赖顺序交给 EXECUTOR，修复后重新验证和复审。自动
修复最多两轮；相同问题持续存在时可以换新 EXECUTOR，也可以直接询问用户，不强制重建
session。

验证或复审发现问题时，有剩余 cycle 就进入 FIX，否则进入 WAIT_USER；修复后的验证通过
进入 RE_REVIEW。FINAL_REVIEW 的输出也先进入 ADJUDICATE，干净后才进入 FINAL_VALIDATE。

`review_only` 在全部 contract 完成、findings 已裁决且无 deferred 后进入 DONE，accepted
finding 作为审核交付保留。`implement` 还要求无 open accepted finding 且最终验收通过。
需要决定时进入 `WAIT_USER`；取消或无法继续时进入 `STOP`。

进入 WAIT_USER 时，`wait` 至少保存 `reason` 和被阻塞的 `resume_state`；恢复后清空 wait。

## 失败恢复

普通查询或传输错误可以重试一次。若 `paseo run` 返回结果不明确，先用 task/role label
查询并 inspect 已有 agent；无法唯一确认时询问用户，不要再创建第二个写入 agent。

Paseo 不可用且用户未强制要求时，可以退出编排并由主代理继续；若用户明确要求 Paseo，
则报告阻塞。外发遵循 `AGENTS.md` 的集中授权边界。
