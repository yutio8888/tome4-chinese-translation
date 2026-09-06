# Tome4 汉化仓库代理说明

本文件适用于整个仓库。

## 任务入口与按需读取

先按用户当前目标区分只读审查、普通维护与正式生产批次；范围、有界批数、暂停和既有授权以当前会话为准。
主代理可直接完成只读检查和小型有界维护，不因任务涉及审核、源码查询或规则文档就自动启动 Paseo。
需要多步实现和独立复审的大型任务、正式生产审核或用户明确要求的编排，按下文采用 Paseo。

只读取当前任务需要的资料：操作与验收查 [`docs/agent-workflow.md`](docs/agent-workflow.md) 对应章节；
译文工作查术语使用规则和相关条目；使用汉化工具时查 [`i18n/README.md`](i18n/README.md) 对应命令；
特殊编辑、提取或发布操作查 [`docs/lessons-learned.md`](docs/lessons-learned.md) 对应教训。
同一任务已读且未变化的资料不重复读取。独立 reviewer 只读其角色契约允许的冻结输入和引用资料。

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
路由，归档正文中的旧触发条件不再生效。需要委托 agent 的实现、源码侦察和独立复审只通过 Paseo 的
ORCHESTRATOR／EXECUTOR／REVIEWER／SENIOR_REVIEWER／SCOUT 角色完成。门禁和普通
检查仍可由主代理作为工具直接调用，不视为启用已归档 Skill 或激活 Paseo。

规则维护任务可由任务指定的唯一写入者修改已明确授权的规则文件；Paseo 激活时该写入者仍为
EXECUTOR，SPEC 与允许文件须明确列出 `AGENTS.md` 或 `.ai/roles/` 下的具体目标。
REVIEWER 始终只读；规则修订不自动扩大其他活动任务的权限，也不追溯改写其冻结记录。

## Paseo 轻量编排（大型任务）

当前已核验的 Paseo 0.4.0（CLI 或等价注入的 agent-scoped Paseo MCP 操作）用于上述编排任务。任务级 orchestration_transport 在 STATE 中只允许 cli|mcp，两种传输必须保持相同的 role、purpose、workspace、lineage、歧义恢复和 reviewer 只读语义。用户明确要求 Paseo 时必须使用；否则 Paseo 不可用时，只有尚未创建 child 或全部 child 已确认归档才可回退主代理执行并说明，仍有未确认归档 child 则进入 WAIT_USER。角色 prompt 见 .ai/roles/，轻量设计说明见 docs/paseo-orchestration-v2-contract.md；活跃的 translation_contextual_v1、translation_contextual_v2 与 translation_surface_screen_v1 候选身份、envelope 冻结与派发契约分别见 docs/paseo-translation-context-review-v1-contract.md、docs/paseo-translation-context-review-v2-contract.md 和 docs/paseo-translation-surface-screen-v1-contract.md（`tools/paseo_contract_check.py` 同时校验这四份契约文件）。现有 v1 task 不迁移；v2 与 surface v1 只供 schema 5 及以上的新 task 使用。活跃角色或契约修改后运行 `python3 -B tools/paseo_contract_check.py`；该检查只证明版本、条款声明和引用有效，角色权限、流程语义与实现是否一致仍需人工核对。

Paseo 角色行为、最小规则、任务记录格式和外发边界的完整定义见 `docs/paseo-orchestration-v2-contract.md`；本文件只保留启用条件与不变量。

### 子 agent 终态判定不变量

判定 child 挂起、调用 stop／cancel 或宣布任何故障结论之前，必须先取得可核验的事实，
不得只凭单一 `status` 字段或某个字段长时间未变就下结论：

- 传输状态面可能过期。除 `status` 外还要读 `attentionReason`／`attentionTimestamp` 与
  activeTurn（为空表示没有进行中的运行），并在动作前重新查询一次。
- 必须检查工作树：`git status --short` 与 `git diff --stat`。未产出任何改动的 EXECUTOR
  留下空 diff，这一条即可区分「什么都没做」与「做到一半卡住」。
- 只有在重新查询后确认仍有进行中的运行且无进展时，才可按挂起处理；字段陈旧本身不是挂起证据。

EXECUTOR 结束但未产出工作成果（无 diff、无报告，或只回了计划／进度说明）时，该次
dispatch 的输出无效：按单次运行规则先归档，再创建 fresh retry child，保持相同 role、
purpose、workspace 与 lineage。已结束的 child 即使仍为 idle 且尚未归档，也不得发送
follow-up 续跑——一次运行结束就不是可继续的会话。

任何已写入记录的故障归因一旦被事实推翻，必须在同一轮立即更正记录并向用户说明，
不得让已撤回的诊断留在 STATE、review 记录或交接文档中。

## 连续批次模式（默认）

在用户已授权的连续译文复核任务内，ORCHESTRATOR 默认
**连续运行**：一个批次进入 `DONE` 并提交后，直接按既定推进顺序选择下一个有界切片并开始，
不需要用户逐批批准。每批结束给出简报即可，不必等待回复。
用户指定的批数、切片、暂停或当前交接中的有界安排优先于此默认；不从历史继续指令推导新授权。

连续运行只改变「是否需要逐批确认」，不放宽任何其他规则。每一批仍须完整执行：受跟踪
`evidence/` 的工作集冻结与逐条源码核验（DLC 来源未固定时如实标注）、SPEC／PLAN／SCOPE／STATE 记录、适用的实现与独立
复审角色分离、候选冻结与 preflight、适用门禁的完整覆盖、`ai_state_check.py` 的
`DONE_VERIFIED`，以及子 agent 生命周期与归档纪律。任何一项不得因为「为了连续」而跳过或延后。

### 必须停下并交回用户

以下停止条件适用于正式批次；普通维护按工作流的完成标准交付。既有授权在其范围内持续有效，
不重复请求确认；需要用户决定时先完成不依赖该决定的范围内工作，交付证据和具体选项。

- 同一 revision 在两轮独立复审之间出现相互矛盾的实质意见（重复实质分歧）。
- 需要尚未授权的术语库改动、全局重命名或跨批次统一策略决定。
- 门禁失败且一次有界诊断无法归因。
- 子 agent 生命周期无法确认：归档预算耗尽后仍无法确认归档状态、歧义创建无法 reconciliation，
  或复审所需的 model 身份在重试后仍无法确定。
- 修复轮次达到 `max_cycles` 仍未收敛（异常路径；正常批次应由下述收敛下限收束）。
- 连续两个 EXECUTOR dispatch 都没有产出工作成果。
- 需要尚未授权的 push、开 PR、发布或对发布仓库、平台的外部写入。
- 批次边界或范围存在实质歧义，不同解读会导致实质不同的工作。

### 自行处理，不必停下

常规修复轮（不超过 `max_cycles`）；按收敛下限收束批次；单次无效 dispatch 的归档与 fresh
retry；按既定顺序选择下一个切片与批次边界；批内专名一致性对齐；执行已授权的术语决定；提交译文
批次与 evidence；按需更新交接和记忆；复审无异议的宿主 advisory。这些都在批次简报中说明，不需要
事先批准。

### 复审收敛下限

以下 lane 数与升级规则适用于 `translation_contextual_v1` implement；v2 的四成员 stage 和默认三轮
按其独立契约执行，不因四个成员提高轮次，`review_only` 不套用 implement 收敛。
v1 复审默认 **2 个并行独立 lane**，`max_cycles` 默认 3；4-lane 是升级路径，只在
一级缺陷出现实质冲突或批次承载机制描述时启用。已接受译文的 reopen 按缺陷分档：

- **一级**：fidelity、completeness、terminology、runtime，以及 placeholder／markup／newline
  不变量。可对固定源码客观判定，任何 cycle 均可 reopen。
- **二级**：grammar、conspicuous translationese。依赖语感、无固定源码判据，只在 `cycle <= 2`
  可 reopen；`cycle >= 3` 起一律只记 advisory。

某个 cycle 不产生一级 confirmed finding 即视为收敛，直接进入最终全量复审，不再开新修复轮。
一个 cycle 的全部 confirmed finding 合并为一次 EXECUTOR 修复 dispatch。新建译文 `implement`
任务一律 `schema_version >= 4`。分档细则、4-lane 升级条件与 `declined_scope` 记法见
[`docs/agent-workflow.md`](docs/agent-workflow.md)。

## 汉化工具入口

- 汉化 CLI 统一使用 `python3 -B tools/i18n <command>`；首次使用该工具环境、依赖或来源配置变化、相关运行失败时执行 `doctor`。只读文档任务不要求运行；正式流程或完整门禁自身要求的 doctor 仍由其入口执行，不在外层重复。译文修改后执行严格 `lint`。工具与报告只在任务允许的边界内工作，派生文件写入已忽略的 `.artifacts/i18n/`。
- 可重生成的 derived 工具产物可留在被忽略的 `.artifacts/`；含人工判断或不可重生成核验锚点的 adjudicated 产物必须写入受跟踪的 `evidence/`。
- 翻译 proposal 必须经 `tools/i18n proposal --strict` 校验；主代理自行检查与委托角色的适用边界见上文，不以工具名推断已归档 Skill 可用。
- Lua 仅按 Lua 5.1／LuaJIT 运行；使用 manifest、`TOME_LUAJIT` 和 `TOME_LUAROCKS_ROOT`，直接 Lua 调用也必须在同一次调用中配置搜索路径。LPeg 固定为已验证的 0.10.2；不得退回新版 Lua。
- 审核、修复和门禁操作步骤见 [`docs/agent-workflow.md`](docs/agent-workflow.md)；Lua、提取器兼容设置、依赖命令与工具／manifest 说明见 [`i18n/README.md`](i18n/README.md)。

## DLC 源码输入（GPL v3 公开）

- ToME4 与三个官方 DLC 为 GPL v3（or later）公开源码，可以直接读取、分析和提取；manifest 固定 engine／extractor 的 commit、组件映射及 DLC 提取基线的快照哈希／条目数，但不固定 DLC 源码仓库、源码 commit 或 1.7.4 源码版本；不在文档中固定本机路径。
- 分发译文／addon 时保留版权声明、使用 GPL v3 兼容许可并提供对应源码。公开源码可由 Paseo 的 REVIEWER／EXECUTOR／SCOUT 及主代理按外发边界只读核验。

## 文档权威顺序

本文件补充全局规则，不覆盖系统／开发者指令或用户当前明确授权。仓库文档之间，授权与不变量以本文件为准；激活时的 Paseo 契约、适用的
[`docs/agent-workflow.md`](docs/agent-workflow.md) 和 [`i18n/README.md`](i18n/README.md)
依次承载下层约束与操作细节，均不得放宽上层规则。任何下层文档与本文件冲突时，
以上位规则为准。

## 门禁触发

按 [`docs/agent-workflow.md` 的验证矩阵](docs/agent-workflow.md#验证矩阵)选择检查，依据任务影响范围而非文件名扩大验证。
五步检查及术语审计是覆盖要求，完整门禁已覆盖时不另跑一遍。正式生产批次保留消费者要求的完整门禁、构建、证据与状态闭合；不得仅改文档绕过工具要求。
只读与纯文档任务核对相关事实、链接、命令和空白；角色或契约变更追加契约检查及语义核对。
普通维护的检查选择依据可写在交付说明中，不为此单独创建 SPEC。

## 任务完成

只读审查以证据、问题状态和调整建议交付为完成，不要求先修复问题。实现任务须满足范围内验收、
解决全部已接受问题并通过适用验证；非阻断 pending／advisory 不自动扩大范围或触发下一轮。
正式任务还须满足其契约的复审、证据、提交／finalize 和生命周期要求；普通任务不借用正式批次的完成谓词。
提交、交接与整理按[工作流完成标准](docs/agent-workflow.md#完成交付与整理)执行；不以清空用户既有改动作为完成条件。

## 校对判定依据

- 当翻译、术语、审核意见或英文表面含义对游戏机制的描述存在分歧时，对 manifest 已固定 commit 的源码以其实际行为为最终判定依据；对来源未固定的 DLC，必须以实际可核验的公开源码证据为准并标明来源未固定。现有译文、术语库和模型 finding 都不能覆盖源码事实。
- 核验机制时应记录对应组件、公开源码路径、适用的固定 commit（若有）和关键调用或数据定义；若来源或 commit 未固定，必须明确记录并标为待确认，据此确认、部分确认、撤销或修订审核结论。当前工作树与固定 commit 不一致时，默认以版本清单固定的 commit 为准，除非用户明确指定其他目标版本。
- 公开游戏与三个官方 DLC 源码可以直接核验；未公开组件只使用用户授权的证据。证据不足时标为待确认。

## 术语库工作流

- 主代理首次开展译文工作时阅读 `TERMINOLOGY.md` 使用规则，随后按词、类别、section 和 source_tag 查询 `terminology/` 相关记录，不要求每次通读目录。独立 reviewer 按冻结输入契约读取。
- 主代理可主动登记具体术语／专名疑点并按 claim 核验，也可裁决 reviewer observation；不强制等待模型先提出疑点，不得用术语库覆盖源码事实。
- 新增或修改高复用术语时，先更新 `terminology/`，再修改对应的 Lua 翻译文件。
- 保留现有 `t(...)` 第三个参数作为 `source_tag`，并为术语填写 `T.*` `category`；不能只按英文原文做全局替换。
- 同一个英文词在不同 section 或 `source_tag` 下可以有不同译法，必须在 `notes` 中说明语境。
- 修改术语后，用 Lua 5.1/LuaJIT 加载现有翻译文件检查 `source`、`target` 和 `source_tag` 是否仍然有效。
- 术语快照自 `production-review-v2-lite-rules-v2` 起不再进入 entry revision identity：纯术语行变更不会使无关条目的既有复审状态失效，只需按实际改动的 target 建立有界 workset。术语快照仍作为 catalog／envelope／evidence provenance 保留。术语库与跨批次策略改动遵循既有授权，超出授权时交回用户；identity-v2 不自动授予新的策略变更权限。
