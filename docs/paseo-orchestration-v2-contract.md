# Paseo 轻量编排 v2 设计

> 状态：设计草案，待实际任务验证。
>
> 契约版本：`paseo-orchestration/2.0-draft`。
>
> 上位规则：[`AGENTS.md`](../AGENTS.md)。本文不单独授权外部传输，也不表示新的控制器
> 或 STATE 校验器已经实现。

本文面向个人翻译项目。目标是用 Paseo 获得“一个 agent 实现、另一个 agent 复审”的
收益，而不是建设企业级工作流平台。设计优先考虑操作简单、失败后容易人工接管，以及
不破坏已有工作树。

---

## 一、设计取舍

### 保留的约束

1. 同一 workspace 同时只有一个任务内容写入 agent；ORCHESTRATOR 可写编排记录和验证产物。
2. 主代理定义范围、独立验证并裁决 finding。
3. REVIEWER 不使用 main workspace；翻译 semantic v2 继续走现有 blind runner。
4. 自动修复最多两轮，仍不能收敛时交给用户决定。
5. 任务开始前记录工作树，结束前运行适用门禁。
6. Paseo 激活期间角色路由独占，不并行使用旧项目 Skill 或其独立 agent。
7. EXECUTOR／REVIEWER 必须是当前 ORCHESTRATOR 的 Paseo-managed child，并出现在其
   Subagents track；provider 原生 subagent 不得代替这两个角色。
8. DeepSeek V4 Flash EXECUTOR 固定使用 `max` thinking，不接受 provider 默认值或静默降级。

### 明确删除的复杂度

v2 不要求：

- 专用 `tools/paseo-orchestrate` 控制器；
- workspace 级文件锁或多控制器并发保证；
- operation WAL、逐动作 revision 和完整 transition history；
- immutable artifact、父子 hash 链或 outbound payload manifest；
- REVIEWER 输入的固定字节数／文件数上限；
- staged、symlink、TOCTOU 和特殊文件的独立 schema；
- 权限轮询、故障注入矩阵或每一步清理失败状态；
- 为实现编排工具另行申请 bootstrap 授权。

这些能力只有在实际遇到重复故障时再增加，不作为首版前置条件。

### 非目标

- 不让模型自动裁决 finding 或替代主代理验收。
- 不让 Paseo REVIEWER 承担 translation semantic observation v2。
- 不自动 commit、stage、reset、删除用户改动或重启 Paseo daemon。
- 不迁移或重解释已有 flat `.ai/task/`、`.ai/reviews/` 记录；新任务写入自己的子目录。

---

## 二、角色

| 角色 | 责任 | 写权限 |
| --- | --- | --- |
| ORCHESTRATOR | 范围、委托、验证、裁决、用户沟通 | `.ai/task/`、`.ai/reviews/` 和验证产物；不改任务内容文件 |
| EXECUTOR | 实现 SPEC 中的修改并运行 focused tests | 允许文件；不得 commit、stage 或修改编排记录 |
| REVIEWER | 独立审查代码、工具、测试和文档 | 不写 main workspace；只返回 findings |

EXECUTOR 和 REVIEWER 都不继承主会话。briefing 必须包含任务范围、验收标准和完成当前角色
所需的上下文，避免依赖隐含信息。

Paseo 在任务明确采用本流程并建立 task ID 时激活，到 `DONE`／`STOP` 或明确记录回退时
结束。激活期间不得使用 `$tome4-pi-review`、`$tome4-pi-file-review`、
`$tome4-pi-subagent`，也不得把这些 Skill 产生的 reviewer/subagent 输出当作 Paseo
contract 结果。ORCHESTRATOR 仍可直接调用 blind translation runner、门禁和普通检查；
这些是角色执行的工具，不是另一套 agent 路由。

---

## 三、模式与审核路由

任务模式只有两种：

- `review_only`：只形成并裁决 findings，不自动修复。
- `implement`：实现、验证、独立复审，必要时最多修复两轮。

审核类型可以有一个或两个：

- `code_legacy_v1`：Paseo Codex REVIEWER 接收代码／工具／文档 diff。
- `translation_v2`：ORCHESTRATOR 直接运行现有 `tools/i18n review` 与 blind v2 runner
  生成 observation，不启用 `$tome4-pi-review`。

混合任务可以共用 task ID、SPEC 和 STATE，但必须分别运行两种审核，不能把术语、Facts 或
历史 finding 注入 blind translation v2 输入。

---

## 四、轻量状态机

### 仅审核

| 当前状态 | 事件 | 后继状态 |
| --- | --- | --- |
| `PLAN` | 审核开始 | `REVIEW` |
| `REVIEW` | 全部 contract 输出返回 | `ADJUDICATE` |
| `ADJUDICATE` | findings 已裁决且无 deferred | `DONE` |
| 任意非终态 | 需要用户决定 | `WAIT_USER` |
| 任意非终态 | 用户取消或无法继续 | `STOP` |

`review_only` 的 DONE 表示 findings 已冻结，不表示没有 finding。

### 实现任务

| 当前状态 | 事件 | 后继状态 |
| --- | --- | --- |
| `PLAN` | EXECUTOR 已创建 | `IMPLEMENT` |
| `IMPLEMENT` | EXECUTOR 完成 | `VALIDATE` |
| `VALIDATE` | 初次实现的定向验证通过 | `REVIEW` |
| `VALIDATE` | 修复后的定向验证通过 | `RE_REVIEW` |
| `VALIDATE` | 验证失败且仍有剩余轮次 | `FIX` |
| `VALIDATE` | 验证失败且轮次耗尽 | `WAIT_USER` |
| `REVIEW` / `RE_REVIEW` / `FINAL_REVIEW` | 全部 contract 输出返回 | `ADJUDICATE` |
| `ADJUDICATE` | 存在 deferred finding | `WAIT_USER` |
| `ADJUDICATE` | 有 accepted finding 且轮次未耗尽 | `FIX` |
| `ADJUDICATE` | 有 accepted finding 且轮次耗尽 | `WAIT_USER` |
| `FIX` | 修复完成 | `VALIDATE` |
| `ADJUDICATE` | initial／re 无 accepted/deferred finding | `FINAL_REVIEW` |
| `ADJUDICATE` | final 无 accepted/deferred finding | `FINAL_VALIDATE` |
| `FINAL_VALIDATE` | 所有 AC 与适用门禁通过 | `DONE` |
| `FINAL_VALIDATE` | 失败且仍有剩余轮次 | `FIX` |
| `FINAL_VALIDATE` | 失败且轮次耗尽 | `WAIT_USER` |
| 任意非终态 | 需要用户决定 | `WAIT_USER` |
| 任意非终态 | 用户取消或无法继续 | `STOP` |

`cycle` 在每轮 FIX 开始时增加，最大值为 2。门禁失败与 reviewer finding 共用这两轮，
避免形成两个独立循环。FINAL_REVIEW finding 和 FINAL_VALIDATE 失败也受相同轮次限制。
进入 WAIT_USER 时，STATE 的 `wait` 保存简短 `reason` 和 `resume_state`；用户决定后恢复到
该状态并清空 wait，不需要通用 decision schema。

---

## 五、任务记录

继续复用现有 ignored 目录，每个 v2 任务使用独立子目录；`task_id` 必须匹配
`^[a-z0-9][a-z0-9._-]{0,63}$`：

```text
.ai/task/<task_id>/SPEC.md
.ai/task/<task_id>/PLAN.md
.ai/task/<task_id>/BASELINE.patch             # 仅在修改既有 tracked 脏文件时
.ai/task/<task_id>/baseline/                  # 仅在修改既有 untracked 文件时
.ai/task/<task_id>/STATE.json
.ai/reviews/<task_id>/review-NN.json
```

已有 legacy flat 文件保持原路径和内容。新任务不得复用已有 task ID，也不得覆盖其他任务的
STATE 或 review 记录。

### SPEC 与 PLAN

SPEC 必须写明：任务模式、范围、允许修改文件、禁止扩展项和可执行验收标准。PLAN 只记录
主要步骤和依赖；实现中发现事实变化时直接修订，不维护 `plan_rev` 或 delta 日志。

### 最小 STATE

```json
{
  "schema_version": 2,
  "task_id": "example-001",
  "mode": "implement",
  "review_contracts": ["code_legacy_v1", "translation_v2"],
  "state": "PLAN",
  "review_phase": null,
  "pending_review_contracts": [],
  "completed_review_contracts": [],
  "cycle": 0,
  "max_cycles": 2,
  "workspace_id": "...",
  "orchestrator_agent_id": "...",
  "baseline": {"patch": null, "copies_dir": null},
  "executor": {"provider": "pi", "model": "deepseek/deepseek-v4-flash", "thinking": "max", "agent_id": null},
  "reviewer": {"provider": "codex", "model": "...", "agent_id": null},
  "open_accepted_findings": [],
  "deferred_findings": [],
  "review_records": {},
  "wait": null,
  "last_error": null,
  "updated_at": "2026-08-13T00:00:00Z"
}
```

STATE 在阶段变化、每个 review contract 完成、agent ID 变化、cycle 增加或出现错误时更新。
`review_phase` 只允许 `initial|re|final|null`。进入新 review phase 时先清空 completed 与
`review_records`；initial／final 的 pending 初始化为全部 contract，re 只列受本轮修复
影响的 contract。每完成一类审核就从 pending 移入 completed，pending 为空后才进入
ADJUDICATE。只校验以下不变量：

1. `state` 属于本文状态集合，且与 `mode` 相容。
2. `cycle <= max_cycles`。
3. 同时最多存在一个活动 EXECUTOR。
4. pending 与 completed 不重复，且都属于 `review_contracts`。
5. `review_only` 进入 DONE 前全部 contract 已完成、findings 已裁决且无 deferred；accepted
   finding 保留在 review 记录中，不放入 `open_accepted_findings`。
6. `implement` 进入 DONE 前还必须无 open accepted finding，并通过最终验收。
7. `review_records` 是当前 phase 的 contract→相对路径映射；其键必须等于 completed，目标
   必须是当前 task 的 review 记录，且记录内 task ID 一致。
8. WAIT_USER 时 `wait` 必须包含 `reason` 和 `resume_state`；其他状态下 `wait` 为 null。
9. provider、model、`orchestrator_agent_id` 和已创建 agent 的 ID 非空。
10. 每个已创建 EXECUTOR／REVIEWER 的 `paseo.parent-agent-id` 必须等于
    `orchestrator_agent_id`；不匹配的 agent 不属于本任务角色。
11. EXECUTOR 的 model ID 以 `deepseek-v4-flash` 结尾时，STATE 的 `thinking` 和
    `paseo inspect --json` 返回的 `Thinking` 都必须为 `max`。

不要求 history、artifact ref、文件 hash 或原子目录同步。普通“写临时文件后 replace”足以
避免 STATE 半写入。

### Review 记录

每份 review 记录必须保存 `task_id`、`review_contract`、`review_phase`、`cycle` 和该
contract 的完成状态。`review-NN` 在 task 内取下一个序号，不覆盖旧记录；当前 contract
到相对路径的映射写入 STATE 的 `review_records`。每个 finding 保存 ID、severity 建议、
file/location、problem、evidence、impact、建议修复和主代理裁决。`rejected` 写一句理由；
`deferred` 说明需要用户决定的事项。复审时逐条标记 accepted finding 为 `fixed` 或
`unfixed`。

---

## 六、Paseo 0.3.1 调用

开始任务时确认当前主代理是 Paseo 托管的 ORCHESTRATOR，再确认版本和可用模型：

```text
test -n "${PASEO_AGENT_ID:-}"
paseo --version
paseo status --json
paseo provider ls --json
paseo provider models --thinking --json <provider>
paseo workspace ls --json
```

EXECUTOR 的初始 prompt 是 positional 参数；后续消息可以使用文件：

```text
paseo run --background --provider pi --model deepseek/deepseek-v4-flash --thinking max
  --workspace <workspace-id> --label task_id=<task-id> --label role=executor
  --json <rendered-prompt>

paseo send --no-wait --prompt-file <prompt-file> --json <agent-id>
paseo wait --timeout <seconds> --json <agent-id>
paseo inspect --json <agent-id>
```

`paseo run` 必须由该 ORCHESTRATOR 进程直接执行并保留 `PASEO_AGENT_ID`。CLI 会把它作为
`callerAgentId` 发送给 daemon，daemon 再为 child 写入
`paseo.parent-agent-id=<orchestrator-agent-id>`；`task_id` 和 `role` label 本身不能建立
父子关系。不得用 provider 原生 `spawn_agent` 创建 EXECUTOR／REVIEWER，也不得在正常路径
手写保留的 parent label。

每次 `paseo run` 返回精确 agent ID 后，必须立即 inspect 并确认 ParentAgentId 等于 STATE
中的 `orchestrator_agent_id`。DeepSeek V4 Flash EXECUTOR 还必须确认 `Thinking` 为 `max`；
缺少 `max`、实际值较低或设置失败都按基础设施错误处理，不得静默降级。不匹配时停止该
agent，不进入下一状态。REVIEWER 即使使用独立 local workspace，也必须保留 parent lineage；
因此它在 UI 中仍属于当前 ORCHESTRATOR 的 Paseo Subagents track，并使用 Paseo agent 的
归档操作。

代码 REVIEWER 使用独立 local workspace。Codex `auto-review` 在 Paseo 0.3.1 中实际是
`workspace-write`，因此不能把 main workspace 交给它：

```text
paseo run --provider <provider> --model <model> --mode auto-review
  --new-workspace local --cwd <review-directory>
  --label task_id=<task-id> --label role=reviewer
  --label review_kind=<initial|re|final> --json <rendered-prompt>
```

完成后按精确 ID 归档即可：

```text
paseo stop --json <agent-id>
paseo archive --json <agent-id>
paseo workspace archive --json <workspace-id>
```

idle agent 不必先 stop。归档或清理失败记录为 warning，不阻止已经通过内容验收的任务进入
DONE；仍在运行且可能写 main workspace 的 EXECUTOR 除外。

---

## 七、简单恢复规则

查询、wait 或 send 的临时错误可以重试一次。`paseo run` 返回超时或连接中断时不要立即
再次创建 agent，先查询：

```text
paseo ls --global --label task_id=<task-id> --label role=<role> --json
paseo inspect --json <agent-id>
```

- 唯一匹配且身份正确：继续使用。
- 无匹配：允许重新创建一次。
- 多个匹配或身份不清：进入 WAIT_USER。

恢复到唯一匹配的 DeepSeek V4 Flash EXECUTOR 时还要检查 `Thinking`。若不是 `max`，必须先
运行 `paseo agent update <agent-id> --thinking max` 并重新 inspect；更新或复验失败时记录
基础设施错误，不发送新的任务消息。

这是唯一需要专门处理的非幂等窗口；不为它引入 WAL。个人项目默认只有一个编排进程，
不支持多个终端同时启动同一 workspace 的 EXECUTOR。

Paseo 不可用且用户没有强制要求使用时，主代理可以直接接管；已有 agent 应先停止。用户
明确要求 Paseo 时则报告阻塞，不悄悄更换执行方式。回退必须先在 STATE 记录原因并结束
Paseo 激活状态；之后才可使用非 Paseo 工作流或旧项目 Skill。

---

## 八、Review 输入与输出

代码 REVIEWER 接收：

- SPEC、相关 PLAN 和验收标准；
- 相对仓库路径表示的、与 `code_legacy_v1` contract 相关的完整 baseline→current 任务 diff；
- 任务前已有改动的排除说明；
- re-review 时 accepted findings 的重验清单。

原始译文 diff 不发送给 code-only REVIEWER；译文只通过 translation v2 blind bundle 外发。

输入应足够小，使 REVIEWER 能完整阅读。超出模型上下文或人工可读范围时按组件拆成新的
task ID，不在同一 review contract 内维护分片状态；不计算固定 512 KiB 或 100 record
阈值，也不需要 override decision。二进制或无法用文本审查的内容由主代理直接验证或
使用专用工具。

REVIEWER 只返回有证据的可行动 finding。模型 severity 和 verdict 是建议；主代理必须
查看实际文件或调用链后决定 `accepted`、`rejected` 或 `deferred`。

旧项目 Skill 的 code review、file-reading review、scout 或 plan-reviewer 输出只能用于
Paseo 激活前的工作；激活后不得执行，也不能据此把任何 pending contract 标为 completed。

translation v2 的 bundle、身份校验和 observation 契约继续以
`docs/pi-review-v2-contract.md` 及现有工具为准，本文不重复定义。

---

## 九、验证与完成

### 实现前

- 记录 `git status --short`、实际 changed/untracked 文件和任务前已有改动。
- 任务前脏文件默认不交给 EXECUTOR。SPEC 确需修改既有 tracked 脏文件时，先把该文件相对
  HEAD 的 patch 保存到当前 task 的 `BASELINE.patch`；既有 untracked 文件复制到当前
  task 的 `baseline/`。这些文件用于中断恢复，不要求全仓 hash。
- 不得清理、reset 或覆盖用户原有改动。

### 每轮实现后

- 核对实际修改文件没有超出 SPEC。
- 对允许修改的既有脏文件，用起始 patch／副本重建任务起点，生成 baseline→current 的
  任务自身 diff；确认用户原有内容未被意外覆盖。相应 reviewer 也接收这份任务自身 diff，
  而不是混合了旧改动的 HEAD→current diff。
- 运行最接近改动的 focused tests 和静态检查。
- 涉译文时遵循 `AGENTS.md` 的门禁顺序；术语改动追加规定审计。

### 完成前

1. 做一轮新的独立复审。
2. 运行最终 AC、适用门禁、构建和 smoke。
3. implement 模式确认没有 open accepted/deferred finding；review_only 只要求无 deferred。
4. 报告变更文件、测试结果和 known issues。

工作树自上次完整门禁后未变化时可以复用结果，不要求额外 hash artifact；主代理必须能
明确说明复用期间没有内容变化。

---

## 十、外发与兼容

常设授权沿用 `AGENTS.md`：通过现有 blind runner 发送 translation v2 bundle；向 Codex
REVIEWER 发送与 code/legacy v1 审核相关的代码、文档和必要上下文；向 pi EXECUTOR 发送
任务 briefing 并允许其读取 workspace。每次任务记录 provider、model 和大致内容范围
即可，不保存完整 payload 或字节计量。

其他 provider 或范围外内容仍须用户授权。外部源码读取仍受对应 Skill 和项目公开源码
边界约束。

旧 flat STATE 和 review artifact 保持原样，不迁移、不删除；新 task 子目录避免覆盖。
若未来扩展
`tools/ai_state_check.py`，它只需按 `schema_version` 区分旧格式和本文最小 v2 格式；旧
格式不能自动改写为 v2。

实现任何可选辅助脚本属于普通项目改动：用户要求实现时按现有审核与门禁流程完成，不
需要额外 bootstrap 授权。

---

## 十一、验收

本文本身的交付标准：

- Paseo 示例命令与本机 v0.3.1 `--help` 一致；
- 与 `AGENTS.md` 的角色、translation v2 路由和门禁顺序一致；
- 相对链接存在，Markdown 与 `git diff --check` 通过。

若未来实现辅助脚本，最小验收只需覆盖：

1. initial、re、final 与 validation 失败路径，cycle 上限和两种 mode 的 DONE 守卫；
2. 混合任务逐 contract 的 pending/completed 恢复，以及 WAIT_USER 的 resume_state；
3. 连续两个 task ID 与 legacy flat 记录并存时互不覆盖；
4. EXECUTOR 唯一性、DeepSeek V4 Flash 的 `max` thinking 校验和未知 `paseo run` 的
   0/1/多匹配恢复；
5. REVIEWER 使用独立 local workspace，且只接收当前 code contract 的任务自身 diff；
6. 允许修改既有脏文件时能从起始 patch／副本区分并保全用户原有改动；
7. 一次 implement dry run、一次 review-only dry run和一次最终独立复审。

`AGENTS.md` 中的轻量 Paseo 流程可以直接使用；本文仍保持设计草案，直到至少一次真实
大型任务验证完成。专用 Controller、复杂 schema 或审计基础设施不再是激活条件。

---

## 十二、修订记录

| 版本 | 状态 | 内容 |
| --- | --- | --- |
| `2.0-draft` | 设计草案 | 面向个人项目的轻量流程；取消重型基础设施，补齐状态闭环、混合审核身份、脏文件基线、角色独占路由、Paseo-managed parent lineage 和 DeepSeek V4 Flash `max` thinking。 |
