---
name: tome4-pi-subagent
description: 使用项目 subagent（scout 源码侦察 / plan-reviewer 计划审查）的入口与边界。scout 用于阅读 t-engine4、DLC 与 addon 发布仓库代码并返回压缩上下文；plan-reviewer 用于对修复/翻译/工具链计划做只读独立审查。Do not use for translation generation or for sending terminology/Facts into blind semantic discovery.
---

# ToME4 项目 subagent（scout / plan-reviewer）

项目 subagent 由 `.pi/extensions/subagent/` 扩展提供，agent 定义在 `.pi/agents/*.md`，
在 TUI 中直接可见并可调度。它们是**只读**的隔离 Pi 子进程：无会话、无项目上下文、
无 skills，工具白名单 `read,grep,find,ls,bash`（`edit`/`write` 永不启用）；结果只作
参考，任何修改都必须由主代理独立完成。首次向外部 provider 发送任务前，必须报告
provider、model、agent 名、任务摘要与可读公开根并取得用户授权；不得用项目级全局
网络放行绕过该授权。

## 调度方式

```typescript
subagent({ action: "list" })                          // 发现可用 agent
subagent({ agent: "scout", task: "..." })             // 前台运行（流式显示）
subagent({ agent: "scout", task: "...", async: true }) // 后台运行 + TUI widget + 日志
```

## scout（源码侦察）

- **用途**：需要了解游戏机制、调用链、DLC 结构或 addon 发布仓库代码时，让 scout
  只读侦察并返回压缩上下文（入口点、关键函数与行号、数据流、风险、建议起点）。
- **任务写法**：写明目标（组件/机制/文件范围）与要回答的问题；要求精确文件路径与
  行号，不贴大段源码。
- **可读根**：项目仓库、`/Users/yun/projects/t-engine4`、`/Users/yun/projects/tome4-dlcs/`
  （ashes/cults/orcs）、addon 发布根（TOME_ADDON_ROOT）。
- **输出**：JSON `{context, files_retrieved, key_code, architecture, start_here, risks, open_questions}`；
  主代理核验路径/行号后再采信，不得直接把 scout 输出当作已确认事实。

## plan-reviewer（计划审查）

- **用途**：动手修复/翻译/发布前，把计划文档交给 plan-reviewer 做只读独立审查：
  可行性、完整性、范围边界、硬约束（AGENTS.md 输入边界/门禁顺序/审核闭环）、风险。
- **任务写法**：把完整计划内联进 task（可引用公开源码路径让 plan-reviewer 自行核验）；
  说明计划要解决的问题与验收标准。
- **输出**：JSON `{findings: [{id, severity, title, body, evidence, scope_ref}], summary}`；
  `severity ∈ {blocker, needs_fix, suggestion, validation_gap}` 只是模型建议，
  定级与处置由主代理独立裁决。

## 边界与授权

1. 只读：scout/plan-reviewer 不得修改、创建、删除任何文件，不得执行 git 写操作；
   bash 不是 OS 沙箱，主代理运行后应独立确认工作树未被改动。
2. 禁止范围：`.artifacts/`、凭据、`~/.pi/`、可读根之外的用户目录；无网络访问。
3. 输入边界：任务/计划文本内联在消息中，不注入术语库、Facts 或 prior findings；
   翻译语义 v2 的 blind discovery 不使用 subagent。
4. 首次外发授权：provider、model、agent、任务摘要、可读根清单必须先行报告并取得
   用户授权。
5. 结果应用：scout/plan-reviewer 的输出只写入会话/日志，不自动应用到规范 Lua 或
   代码；主代理独立校验后按既有工作流应用并跑门禁。
