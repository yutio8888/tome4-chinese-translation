# Contextual Envelope 原子冻结入口：Backlog 记录

> 状态：`backlog / not authorized for implementation`。
> 本文只记录已确认的集成缺口，不改变现有 `translation_contextual_v1` 契约、
> payload、candidate identity、STATE closure 或任何运行入口。

## 问题

当前上位规则要求 ORCHESTRATOR 在冻结或哈希 `translation_contextual_v1` payload
之前，以任务作用域 `SCOPE.json` 和精确七键 draft payload 运行 deterministic
contextual-anchor preflight。该 preflight 证明每个 `translation_snapshot.source` 是
声明章节窗口中真实 `t(...)` 调用的已解码第一个参数。

现状中这仍是 ORCHESTRATOR 的操作纪律：没有唯一的生产冻结入口把以下步骤作为不可分割
操作执行：

```text
draft seven-key payload + SCOPE.json
  -> contextual-anchor preflight
  -> canonicalize / candidate_identity
  -> write CONTEXTUAL-ENVELOPE-<dispatch_id>.json
```

因此手工写 envelope 的路径理论上可以绕过 preflight，产生一个已冻结、却没有被技术验证其
snapshot 与真实 Lua 调用／声明章节窗口对应关系的候选。发现该问题的时点若落在 closure
阶段，REVIEWER 可能已审阅了错误输入，修复已太晚。

## 约束与拟议方向（非实施授权）

- 后续若启动，建立唯一、原子的 contextual envelope freeze 入口；成功 preflight 是写入
  envelope 和计算 identity 的前置条件。
- 不应先在 `tools/ai_state_check.py` 收束时重跑 preflight：那时的当前 Lua 工作树可能已不同于
  envelope 冻结时的输入，必须先定义 Lua 与 `SCOPE.json` 的快照／身份绑定语义。
- preflight 不得改变 reviewer 可见七键 payload、candidate identity、review JSON 或 STATE
  closure identity；这些边界保持现有契约定义。
- 本 backlog 不涉及 `candidate_author_agent_id` 的离线 closure，也不涉及 STOP lifecycle
  predicate、Paseo runtime 路由或 GitHub Issue #3 的 LuaJIT/LocaleLoader scanner 替换。

## 启动条件

只有用户明确授权新的、独立 task 后才可设计或实现。该 task 必须先冻结：入口 API／CLI、
Lua 与 `SCOPE.json` 快照绑定、失败原子性、既有手工 envelope 路径的处置方式，以及覆盖
绕过、篡改、章节边界和成功路径的测试。

## 依据

- [`AGENTS.md`](../../AGENTS.md)：translation contextual preflight 上位规则。
- [`paseo-orchestration-v2-contract.md`](../../docs/paseo-orchestration-v2-contract.md)：当前
  contextual payload／envelope 边界与 preflight 契约。
- [`contextual_anchor_preflight.py`](../tools/contextual_anchor_preflight.py)：当前离线
  fail-closed preflight 工具；工具本身不是冻结入口。
