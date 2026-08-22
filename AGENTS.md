# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 角色与协作

- **主代理**负责范围、裁决、验证和最终交付，通常也是仓库写入者。
- **审核子进程／项目 subagent**只返回 proposal、context 或 findings；其结果由主代理核验后再应用。
- **Paseo 编排**启用时，主代理任 ORCHESTRATOR；EXECUTOR 是任务内容文件的唯一写入 agent，REVIEWER 做常规独立复审，SENIOR_REVIEWER 做第二轮后的范围校准和高影响流程交叉复审，SCOUT 做只读源码侦察（返回压缩代码上下文，不产生审核 contract 结果）。

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

当前已核验的 Paseo 0.4.0（CLI 或等价注入的 agent-scoped Paseo MCP 操作）用于需要多步实现和独立复审的大型任务；小型修改由主代理直接完成。任务级 orchestration_transport 在 STATE 中只允许 cli|mcp，两种传输必须保持相同的 role、purpose、workspace、lineage、歧义恢复和 reviewer 只读语义。用户明确要求 Paseo 时必须使用；否则 Paseo 不可用时，只有尚未创建 child 或全部 child 已确认归档才可回退主代理执行并说明，仍有未确认归档 child 则进入 WAIT_USER。角色 prompt 见 .ai/roles/，轻量设计说明见 docs/paseo-orchestration-v2-contract.md；translation_contextual_v1 的候选身份、envelope 冻结与派发契约另见独立的 docs/paseo-translation-context-review-v1-contract.md（`tools/paseo_contract_check.py` 同时校验这两份契约文件）。活跃角色或契约修改后运行 `python3 -B tools/paseo_contract_check.py`，只检查角色/purpose 约束和固定运行时身份回流。

Paseo 角色行为、最小规则、任务记录格式和外发边界的完整定义见 `docs/paseo-orchestration-v2-contract.md`；本文件只保留启用条件与不变量。

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
