# DSH 编排兼容契约 v1

> 契约版本：`dsh-orchestration-compat/1.0-draft`。
>
> 状态：提议，未启用；仅交付兼容设计，不授权 DSH child 派发或正式生产批次。
>
> 上位规则：[AGENTS.md](../../AGENTS.md)。对照基线：
> [Paseo 编排契约](../../docs/paseo-orchestration-v2-contract.md) `paseo-orchestration/2.25-draft`。

## 1. 目标与启用边界

保留项目的角色分离、候选冻结、源码证据、人工裁决和门禁，允许未来通过 DSH 执行有界任务，
而不是把 Paseo CLI 命令机械改名。DSH 是另一种编排后端，不是现有 `cli|mcp` 传输的第三个取值。

当前 AGENTS.md 仍要求受委托实现、侦察和复审通过 Paseo。本文件不覆盖该要求；编写本草案
也不等于激活 Paseo 或 DSH 编排。主代理仍可按普通维护规则直接完成小型有界任务。

拟分两级接入：

| 级别 | 用途 | 前置条件与结果限制 |
| --- | --- | --- |
| `experimental` | 非生产、有界代码或文档实现／只读检查 | 用户明确授权试验范围，并先修订上位入口、建立 DSH 专用角色与记录校验；结果仅按试验验收，不声称 Paseo 等价 |
| `production-compatible` | 正式译文审核与生产批次 | 补齐本文能力缺口、适配现有消费者与完成检查、通过恢复和负向测试后另行启用；本版不可用 |

已有 Paseo task 不迁移、不改 transport、不转写历史 child 身份。Paseo 有未确认归档 child 时，
不得用 DSH 接管或主代理直写规避关闭要求。换后端必须先按原契约关闭原任务，再新建任务。

## 2. 能力依据与非等价项

本版依据起草会话实际暴露的 DSH 工具定义，不承诺其他版本也提供相同能力。
草案已获用户单次授权，通过默认 Claude job 做过只读审核并收获结果；这不等于标准 `subagent`
角色通道、取消／恢复或工作树隔离已经实测。每次试验须重新核对工具定义，并保存能力核对结果；
缺失接口不得靠提示词或模型自述补齐。

| 项目要求 | 当前 DSH 接口／语义 | 兼容结论 |
| --- | --- | --- |
| 创建独立上下文 child | `subagent`：完整独立 briefing；默认后台，返回 durable agent id，运行结束后通知父代理 | 首选；须另行绑定 task、role、purpose、工作树和父级 |
| 继承父会话 | `subagent_fork` 继承父会话已完成轮次的上下文，不含当前进行中的轮次 | 不用于独立 reviewer；本版也不用于 executor/scout，避免隐含上下文越界 |
| 生命周期发现 | `list_agents` 可列直系或后代及 parent/depth | 可协助追踪，不能把列表当完成事件或待领取结果队列 |
| 可续跑 child | `send_message` 可引导运行中 child，也可启动 idle/ready child 新一轮 | 工具允许不等于项目允许；按第 5 节限制 |
| 中断 | `interrupt_agent` 请求取消当前 turn；不保证立即停止，队列和后代不会一起清除 | 不等于停止整个 agent，更不等于归档 |
| 后台 job | `job_output` 收获、`job_kill` 请求取消；与 agent id 分属不同对象 | 单独记账，不混用 id 或关闭证明 |
| 另一代理接口 | `subagent_claude_code` 默认前台，后台返回 job id | 本版不作为标准角色通道；不能从工具名推断实际 model |
| Paseo role labels／workspace 元数据 | `subagent` 创建参数没有对应强制字段 | DSH dispatch 记录仅为项目声明，不冒充运行时强制绑定 |
| child 工作树绑定 | 当前 `subagent` 参数没有显式 cwd/workspace 选择接口；实际继承行为未实测 | 不以 briefing 或父代理单次 shell 切目录证明绑定，试验写入前按第 4 节核验 |
| live profiles、精确 model、作者 provider 查询 | 当前暴露工具未提供 Paseo 等价查询 | 无法证明精确双模型独立；不填写虚假的 verified |
| archive 与确认查询 | 当前暴露工具没有等价操作 | 逻辑不复用不能写成 `archive_confirmed=true` |
| reviewer 只读权限 | briefing 可约束；当前会话文件策略为 `danger-full-access` | 行为约束不是沙箱隔离，不能声称已强制只读 |

`running` 表示当前正在工作，`idle` 是已加载但轮次间歇，`ready` 是仅持久化、可恢复状态。
三者都不能单独证明输出有效、任务完成或运行时已归档。子 agent 可能等待其后代。

DSH 工具允许的续跑和后台能力不改变项目范围，也不自动授予外发、提交、push、发布权限。

## 3. 保持不变的项目语义

1. ORCHESTRATOR 负责范围、派发、验证、裁决、用户沟通，只写编排记录和验证产物。
2. 同一工作树同一时刻仅一名 EXECUTOR 修改允许的任务内容；父代理不得同时补丁修复。
   修改 AGENTS.md 或角色文件仍须显式列入授权路径。不得覆盖任务前已有改动。
3. REVIEWER、SENIOR_REVIEWER、SCOUT 只读；SCOUT 返回上下文，不代替独立复审。
4. findings 必须引用源码或语境证据，由 ORCHESTRATOR 独立裁为 `confirmed|pending|advisory`；
   仅 confirmed 可进入自动修复，severity 和模型完成声明不构成事实。
5. reviewer 互不读取其他 lane 输出；不得接收父会话、历史裁决或超出其角色契约的材料。
6. 实现前记录工作树基线、允许路径、验收标准、验证命令和轮次上限；派发前冻结 SPEC、
   有界 diff（含任务新建 untracked 文件）及允许读取的引用。候选改变则重新冻结、重新审核。
7. 源码版本、DLC 未固定来源标注、术语授权和外发边界保持现有上位规则；不附送整个父会话。
8. 任务按[验证矩阵](../../docs/agent-workflow.md#验证矩阵)验收。连续运行、有界批数、暂停、
   收敛规则和用户决策边界不因 DSH 改变。
9. 翻译流程／基础设施的 code review 仍由 REVIEWER 与 SENIOR_REVIEWER 对同一候选独立
   交叉审核；第二轮后的普通 finding 仍先做范围校准。SENIOR_REVIEWER 不承担译文审核。
   experimental 无法核验精确模型差异时必须标为未证明，不得声称满足正式双模型要求。

现有 [.ai/roles/](../../.ai/roles/reviewer.md) 含 Paseo 专属身份及稳定条款引用，不得直接当作
已经适配的 DSH prompt。启用前需新建专用模板，逐项保留内容权限并显式替换运行时条款。

## 4. 派发与冻结

拟采用 `subagent` 作为唯一角色创建入口，由当前 ORCHESTRATOR 创建直系 child。
child 不再派发下级 agent 或启动脱离追踪的后台工作；需要额外角色时返回请求，由父代理决定。
工具可见性不等于授权。

每份独立 briefing 至少包含：

- contract version、task id、dispatch id、role、purpose；
- 绝对工作树根、允许写入路径（只读角色为空）、允许读取材料、任务前改动保护清单；
- SPEC／验收标准、冻结候选引用、输入路径和适用输出格式；
- 唯一写入、禁止递归委托、禁止擅自提交／外发、停止条件；
- 必须报告实际工作目录、变更路径、测试结果和未解决项，不以计划替代成果。

创建前先持久化 dispatch intent；成功返回后绑定真实 agent id，再通过直系列表交叉核对。
briefing 中声明的 parent、role 和工作树不是运行时证明；记录须区分“声明”和“观察”。
无法核对时不能宣称严格 lineage/workspace 等价。

experimental 写入前，须在实际绑定到隔离试验树的宿主会话中，以只读探针和可核验工具执行
记录确认 child 的工作目录及路径解析；不能只采信 child 最终文字报告，也不能假定父代理某次
shell 的 `cd` 或 `workdir` 会改变后续 child 的宿主目录。无法确认则不派发写入者，进入 WAIT_USER。
该检查只证明观察到的目录，不证明文件系统沙箱隔离。派发前后分别核对试验树及主仓库树的
tracked/untracked 状态与必要 diff；若两者相同则不是隔离试验。出现树外写入或无法归因的变化时
停止接纳结果，先保存证据和确认生命周期，不自动修复或清理其他工作树。

并行只限相互独立、同一冻结候选的只读角色；不得与候选写入并行。结果必须绑定原候选，
不得将旧 candidate 输出改标为新 candidate。原始结果与裁决分开保存；人工判断及不可重生成
核验锚点写入受跟踪的 `evidence/`，可再生成产物留在 `.artifacts/`。

正式译文接口只作为未来适配目标：
[contextual v1](../../docs/paseo-translation-context-review-v1-contract.md)、
[contextual v2](../../docs/paseo-translation-context-review-v2-contract.md)、
[surface v1](../../docs/paseo-translation-surface-screen-v1-contract.md)。
其 candidate identity、envelope、lane 顺序、严格 raw bytes/schema、full/closure 和收敛要求均不改动；
不能把普通自然语言 DSH 回答包装成有效 review JSON。未通过相应 preflight／消费者验证的输出
仅作试验材料，不写入正式 review 完成记录。

上述边界也适用于代码、工具、流程和文档实现：试验改动若要纳入正式工作树或提交，必须先按
AGENTS.md 及适用的普通维护／Paseo 流程验收，补齐该流程要求的独立复审与门禁；不能把 DSH
试验记录充当 Paseo 复审、双模型或正式批次完成证据。普通维护不因此自动升级为正式生产批次，
提交授权本身也不豁免验收。用户单次授权的草案审核不等于长期启用本契约。

## 5. 单次运行、收获与逻辑退役

本节是拟议的 experimental 生命周期，不是 Paseo 归档的等价实现。

```text
INTENT -> RUNNING -> RESULT_RECEIVED -> VALIDATED -> RETIRED
              \-> CANCEL_REQUESTED -> SETTLED -> RETIRED
任何身份、创建或终态歧义 -> WAIT_USER
```

- 默认后台派发；等待完成通知期间做独立工作，不反复轮询，也不重复运行 child 的任务。
- `subagent` 的结果由完成通知返回；不得拿 agent id 调用 `job_output`。真正的后台 job
  必须保存 job id，并在交付前用 `job_output` 收获仍相关结果；不再需要的 job 请求取消。
- `RESULT_RECEIVED` 只证明收到了结果，不代表通过验收。先保存原始结果，再核对候选、权限、
  工作树变化和测试。只回计划／进度、缺少成果的 executor 输出无效。
- 无效输出或修复下一轮使用新的 dispatch 和 fresh child；第一次无效可有界重试，连续两次
  executor 无成果即交回用户。已结束 child 不用 `send_message` 续跑。
- `send_message` 仅用于仍在运行的 EXECUTOR／SCOUT 当前 dispatch 的必要澄清／收窄；
  不得改变冻结候选或扩大范围，派发记录保存澄清内容。REVIEWER／SENIOR_REVIEWER 派发后
  禁止补充实质提示、侧重点、范围收窄或其他意见；确需澄清时作废本次输出，待旧运行按本节
  安全结束并退役后，冻结完整新输入并 fresh 重派，不能沿用旧 candidate 的完成证明。
  结束竞态导致新 turn 意外启动时立即记录并核实，不把它当合法 fresh retry。
- `RETIRED` 仅表示结果已处理、已观察到该次运行结束、项目不再给此 child 发消息；保留 id。
  它不表示运行时禁止恢复、无排队消息或已归档；记录显式保留这些未证明项。
- experimental successor 只能在上一写入者结束、结果收获、无已知活动后代／job、工作树核对
  且逻辑退役后启动；不能证明没有后续写入风险时进入 WAIT_USER，不继续共享工作树写入。

请求中断前重新取得运行证据，核对 `git status --short`、`git diff --stat` 和当前进展。
DSH 没有暴露 Paseo 的 attention/activeTurn 等字段时记录缺失，不能伪造这些字段，也不能仅凭
耗时或 `idle/ready` 诊断挂起。`interrupt_agent` 成功只代表请求接受，仍须等实际结束证据；
发现后代时先停止派发、核实各运行与 job，不能认为中断父级已清理整个子树。

`SETTLED` 必须有绑定该 agent／dispatch 当前运行的宿主结束通知；后台 job 则须由
`job_output` 返回该 job 的终态（而非 running）。错误或取消终态只能证明该次执行结束，不能
证明成果有效。取消请求回执、列表快照、超时、空 diff 或 child 自称停止均不够；缺少上述
结束证据时记录“运行时终态不可证明”并进入 WAIT_USER，不假定取消一定产生完成通知。
即使已 SETTLED，也要核实后代、job、已发送消息和意外新 turn；未能排除已知后续活动风险时
不得 RETIRED 或派发 successor。`TRIAL_STOP` 同样要求全部 dispatch 安全退役、无生命周期歧义。

中断／失败后的部分写入先保存基线、实际 diff 和路径清单，再区分允许范围内半成品、越权
改动与用户原有改动。半成品不自动成为已接受候选；明确裁决后才可纳入新的修复 briefing 和
冻结输入。禁止 `git reset --hard`、`git checkout .`、`git clean` 等整树清理；定向恢复也必须
先确认旧写入者结束、目标属于授权路径、preimage 可核验且不会覆盖用户改动，否则 WAIT_USER。

只读角色造成任何工作树改动时，记录越权并作废该 dispatch 的输出；先保全证据、处理遗留
改动并确认安全退役，再考虑 fresh dispatch。无法确认变化归属时先标 pending 并暂停接纳，
不能把越权修改当成额外成果，也不能自动回滚用户或其他任务的改动。

工具本身可能允许继续已结束 child；本契约有意采用更严格的一次 dispatch 一次运行策略，
便于复审独立性和恢复审计。逻辑退役不足以解除一个原有 Paseo task 的归档义务。

## 6. 记录、恢复与失败关闭

拟使用独立命名空间 `.ai/dsh-task/<task_id>/` 保存 SPEC、PLAN、SCOPE、STATE 和 dispatch 日志；
这是待实现的格式，不是现有工具已识别的 schema。证据保存在 `evidence/dsh/<task_id>/`。

最小字段组如下；枚举和完整 JSON schema 在适配实现时固定：

| 字段组 | 必须表达的事实 |
| --- | --- |
| task | contract version、`backend=dsh`、`tier=experimental`、task id、模式、状态、授权边界和 max_cycles |
| workspace | 绝对 realpath、基线 commit、任务前 tracked/untracked 改动清单及必要的基线内容 |
| capability snapshot | 当前可用工具、缺失能力、只读隔离等级、身份核验方式；观察依据而非模型推测 |
| candidate | 冻结引用、范围路径、可复现 diff 配方及包含新文件的候选内容；candidate_author 指向主代理／最后实质修改候选的 executor dispatch，既有或来源不明候选记 unknown |
| dispatch identity | 不可变 dispatch id、role、purpose、声明的父级和工作树、candidate binding、retry_of |
| runtime binding | 创建返回的 agent id、直系查询证据、实际可观察元数据；缺失记 missing，不推断 provider/model |
| lifecycle | 创建意图、调用结果、完成／取消证据、原始结果位置、验证结论、逻辑退役、已知后代/job |
| adjudication | finding 证据、confirmed/pending/advisory、接受或拒绝原因及验证结果 |

`candidate_author` 是项目侧溯源声明，不是 provider/model 或运行时身份核验证明。冻结时根据
实际接受的写入记录确定，candidate-bound reviewer dispatch 复制同一指针；冻结期间不可改写，
候选变更时重新确定。它不进入 review JSON 或候选内容 identity，也不能代替独立上下文和模型
差异核验。禁止候选作者承担该候选的独立 reviewer；主代理裁决不冒充独立审核。

不得把 `backend=dsh` 写成 Paseo STATE 的 `orchestration_transport`，不得写入假的 archive、
model diversity proof 或 `DONE_VERIFIED`。本版不新增现有 checker 的可接受值。

创建调用失败／返回不明确时，不立即再次创建：先用持久化 intent 和直系列表核实是否产生了
child；只有无歧义才能绑定或确认未创建。标题相同不能证明同一 dispatch。无法唯一匹配则
WAIT_USER；不得靠重复创建赌一次成功。

会话恢复先读授权、基线、未闭合 dispatch，再核对真实 child/job 和工作树；不从 TODO、
goal 状态、上次自然语言简报推断完成。丢失原始结果或候选漂移时，不重建假结果；确认旧运行
安全结束后才能 fresh retry。被新证据推翻的故障归因同轮修正记录并告知用户。

任务级试验终态拟用 `TRIAL_DONE|TRIAL_STOP`，与 Paseo DONE/STOP 分开。TRIAL_DONE 要求：
验收满足、接受的问题已解决（review_only 则完成裁决而不要求修复）、适用验证通过、结果及
人工证据落盘、全部 dispatch 逻辑退役、无已知活动工作且无生命周期歧义。任一缺失则不宣称完成。

## 7. Goal、workflow 与 Ralph 的边界

- `todo_write` 只是进度面板，不是任务状态或证据账本。
- goal 只承载用户已授权的长任务持续推进；恢复、阻塞和完成仍遵守当前宿主工具规则。
  项目 WAIT_USER 时停止有副作用工作并交回用户，不能为满足自动轮次重复派发或扩大授权。
- `workflow` 仅在用户明确要求 workflow 或大型多 agent 编排时才具备宿主调用条件；
  `ralph` 仅在用户明确要求 Ralph／fresh-agent 迭代时才具备宿主调用条件。
- 上述条件不授权绕过本契约唯一入口：DSH 任务活跃期间，不得通过 workflow／Ralph
  创建本任务角色或任务内容写入者。确需换通道，须先收获结果、安全退役全部 dispatch、
  核实无残留活动并记录任务暂停，随后按用户新授权建立独立范围与适用契约；无法关闭则 WAIT_USER。
  本版不定义这两种通道的适配，其结果不得直接回填本任务的完成记录。

## 8. 启用清单与验证计划

本草案交付不执行以下迁移。Paseo 基线版本变更或 DSH 工具定义变化时，须重新核对兼容结论，
更新本文基线及能力说明；不把旧版本结论自动视为新版本兼容，也不删除固定版本来掩盖漂移。
每次启用前核验该对照关系。后续启用须作为独立有界任务：

1. 用户确认 experimental 的范围和非等价限制；修订 AGENTS.md 的后端选择入口及权威顺序，
   明确旧 Paseo task 不迁移，建立 DSH 专用角色模板，不能只改本文状态。
2. 实现独立 STATE schema／validator，检查角色、路径、候选绑定、生命周期和试验终态；
   未满足 production 能力时，消费者必须拒绝把记录当正式批次。
3. 在无用户未提交改动的隔离试验工作树验证：独立 briefing、唯一写入、冻结候选复审、
   原始结果收获、fresh retry、后台 job 清理与恢复。未运行不能标记通过。
4. 负向测试覆盖：创建歧义、结束竞态、取消尚未完成、候选漂移、越权修改、缺少原始结果、
   后代仍活动、模型身份缺失和两次 executor 无成果；这些场景必须拒绝错误完成。
5. 正式接入前提供可核验的身份／workspace／lineage、精确双模型证明、只读权限控制，以及
   与原归档义务等价的终态关闭机制；或经明确规则修订接受非等价方案，不能暗中降级。
6. 对正式 review preflight、严格 bytes 校验、证据消费者、`ai_state_check.py`、完整门禁、
   finalize／重放建立适配及回归测试。没有这一步，不开放 production-compatible。

纯草案维护按验证矩阵核对事实、引用、命令和空白，并运行
`python3 -B tools/paseo_contract_check.py` 确认未破坏已有活跃契约。
该脚本当前只覆盖 Paseo 的 AGENTS／角色及四份契约；通过不证明本文已被校验，更不证明 DSH
适配实现完成。本版仍需人工语义核对，不运行与纯文档无关的译文构建或生产门禁。
