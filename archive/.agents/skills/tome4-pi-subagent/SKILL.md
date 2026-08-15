---
name: tome4-pi-subagent
description: 仅在 Paseo 未激活时调用项目只读 subagent：scout 侦察 t-engine4、DLC 或 addon 源码，plan-reviewer 独立审查修复、翻译、工具链或发布计划。用于非 Paseo 的源码侦察或计划复审；Paseo 激活后不得使用，改由 ORCHESTRATOR／REVIEWER 承担对应职责。
---

# ToME4 项目 subagent

仅在 Paseo 未激活时执行本 Skill。如果任务已有 Paseo task ID 或已明确采用 Paseo，停止本
Skill；不要调度 scout／plan-reviewer，也不要把它们的输出计入 Paseo review contract。

项目 agent 定义位于 `.pi/agents/`，通过 `.pi/extensions/subagent/` 调度。通用只读
边界、外发记录和结果裁决遵循 `AGENTS.md`；具体可读范围与输出 schema 以对应 agent
定义为准，不在本 Skill 中复制。

## 调度

```typescript
subagent({ action: "list" })
subagent({ agent: "scout", task: "..." })
subagent({ agent: "scout", task: "...", async: true })
subagent({ agent: "plan-reviewer", task: "..." })
```

使用 `scout` 时，在 task 中写明组件、源码范围和要回答的机制问题；要求返回入口点、
调用链、精确路径/行号、风险与未决问题，避免大段源码。

使用 `plan-reviewer` 时，把完整计划内联进 task，并写明问题、范围和验收标准；要求从
可行性、完整性、边界、项目硬约束和验证路径审查。不要让它直接修改计划或生成 patch。

## 处理输出

- 只接受对应 agent 定义声明的 JSON 结构；格式错误时不要猜测补全。
- 路径、行号、机制断言和 findings 由主代理独立核验后再采信。
- subagent 输出只作上下文或审阅意见，不自动写入规范 Lua、代码或计划。
- 非 Paseo translation v2 的 blind semantic discovery 使用 `$tome4-pi-review`，不得
  通过 scout 或 plan-reviewer 注入术语、Facts、历史 finding 或源码上下文。
