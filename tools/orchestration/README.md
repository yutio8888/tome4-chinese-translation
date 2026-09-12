# 审核编排辅助入口

约束以 [AGENTS.md](../../AGENTS.md)、[编排契约](../../docs/paseo-orchestration-v2-contract.md)、
[surface 契约](../../docs/paseo-translation-surface-screen-v1-contract.md)和
[contextual v2 契约](../../docs/paseo-translation-context-review-v2-contract.md)为准。
这些脚本辅助 ORCHESTRATOR 操作，不授予生产批次、译文修复或外部发布权限。

## 支持范围与传输边界

`review_lifecycle.py` 管理 review_only 的 surface full／四 lane 与 contextual v2 full。
它保留每次 dispatch，先核验整组冻结输入，再逐个记录 create intent、首个 live 观测、
通知后的 raw、strict 检查和归档确认。唯一 ORCHESTRATOR 写入同一 children journal；
不要并发运行多个写 journal 的命令，也不要同时手改 STATE。

创建路径为 CLI 或 agent-scoped MCP；完整 live/归档观测使用 **MCP 捕获文件**。
原始终稿支持下述两个已核验版本的原生日志；它只是只读观察来源，不增加生命周期传输。
捕获文件保存 `get_agent_status` 的 `structuredContent` 对象（含 status/snapshot），不用显示文本：
根 `status` 与 `snapshot.status` 一致；身份和运行事实只读 `snapshot` 下的 `id`、
`workspaceId`、`cwd`、`labels`、`activeTurn`、`attentionReason`、`attentionTimestamp`。
归档须看到 `status=closed`、非空 `archivedAt`、无 active turn。首个 runtime observation
只读同层 `provider/model/currentModeId/thinkingOptionId`；null 与 missing 分开保存，
不从 `runtimeInfo`、profile、title 或其他字段补值。

**CLI 创建兼容：**无 `--emit` 的旧位置参数入口恢复为一次 CLI 创建；增加必需的
`--profiles`，由 host 在本次 create 前实时查询并留档。`--provider/--thinking/--mode`
保持；成功持久化 ID 后只返回 `CREATED`，不声称 dispatched。取得完整 live 绑定前不得创建
下一成员。CLI inspect/logs 的显示字段仍不完整；使用 MCP capture 补充观测，不回填旧字段。
任务的 `cli|mcp` 记录实际创建路径，观测来源另记；save 只校验，不改写传输。
已有准备或 child 历史的任务不得换路径。stage 工具初始为 cli；无历史的新任务可在首次准备时
显式传 `--select-transport mcp`，后续调用不再传此选项。旧 journal 缺 creation_transport
不会被猜测或迁移，须由 ORCHESTRATOR 核验，不能自动改历史。

emit 文件是**本地创建参数清单，不是 MCP wire schema**。ORCHESTRATOR 按当前已注入工具的
schema 将 provider/model、settings、workspace、labels 和 prompt 传给 agent-scoped create。
每个 create 前仍须重新读取实时 `list_profiles`、检查 notes 和运行时可用性，并保存该次
原始响应；helper 只能留档该响应，不能替人工判断其时效、notes 或 profile 选择。
provider/mode/thinking 的默认值只是派发建议，不是实际 runtime 身份。

## 从冻结输入到完成记录

以下 shell 占位路径由当前任务指定；children、captures、timing 放任务自己的 ignored 目录。
不运行 queue rebuild/start，不重新冻结已发出的 candidate。STATE 必须已存在、mode=review_only，
task/workspace/contract 正确；`PASEO_AGENT_ID` 为当前直接父代理，workspace 按 cwd 发现，
或显式提供 `TOME_PASEO_WORKSPACE`。`TOME_TRANSLATION_ROOT` 可用于独立 fixture 根。

```bash
# plan/ctx 均来自已完成冻结与 preflight 的输入。
python3 -B tools/orchestration/dispatch_surface.py plan.json children.json --emit emit.json --select-transport mcp
# contextual full 使用相同操作接口：
python3 -B tools/orchestration/dispatch_contextual.py ctx.json ctx-children.json --emit ctx-emit.json --select-transport mcp
```

一次准备会先检查所有 lane 的 envelope、candidate、input SHA、完整 manifest 和 prompt 长度。
准备成功只表示 `prepared`；尚未调用 create。对每个 emit 成员，顺序执行：

```bash
# KEY 的形式为 task_id|dispatch_id。先获取并保存该次实时 profiles.json。
python3 -B tools/orchestration/review_lifecycle.py create-intent children.json "$KEY" --profiles profiles.json
# 上条退出 0 后，立即按输出参数调用一次 MCP create_agent。
# 把首次 get_agent_status 的完整 JSON 对象原样写入 live.json；下一条即时绑定：
python3 -B tools/orchestration/review_lifecycle.py bind children.json "$KEY" --capture live.json
```

CLI 路径则在 stage 的 cli 初始状态下调用（每次最多创建一个成员）：

```bash
python3 -B tools/orchestration/dispatch_surface.py plan.json children.json --profiles profiles.json
# contextual 使用 dispatch_contextual.py，参数相同。
# CREATED 后保存完整 MCP status 对象，立即绑定；成功后才再次实时查 profiles 并创建下一成员。
python3 -B tools/orchestration/review_lifecycle.py bind children.json "$KEY" --capture live.json
```

`--record ids.json` 接受 `{"task|dispatch":"agent-id"}`，只持久化 created ID，缺首个 live
时退出1；随后可用 `--live lives.json` 绑定，形状为 `{"task|dispatch": <完整 status 响应>}`。
失败 capture 在所有检查结束前不改变 row；同一 Journal 内重试也保留首次有效观测。

创建不明确时保留 dispatching。唯一匹配交给 bind；零匹配使用：

```bash
python3 -B tools/orchestration/review_lifecycle.py reconcile-absent children.json "$KEY" --evidence absent-audit.json
# confirmed_absent 后，重新实时查 profiles；同 dispatch 最多再 create 一次。
```

`absent-audit.json` 是 host 核验记录，**不是传输 wire schema**。包含：

- `schema="review-create-reconciliation/1"`、`key`、当前 `create_attempt`、查询时间 `queried_at`；
- `filter={workspace_id,cwd,labels}` 必须与该 journal row 精确一致；`complete=true`、
  `includes_archived=true`、`lifecycle_filter=null`；`excluded_history_ids` 为 journal 所有已知 ID 排序列表；
- `pages` 恰一项，`cursor=null/next_cursor=null/has_more=false`；`request` 为
  `{"tool":"list_agents","arguments":{"includeArchived":true,"cwd":"任务cwd","sinceHours":720,"limit":200}}`；
  `response` 保存原始工具响应，其中 `structuredContent.agents` 是完整列表；
  `snapshots` 为该列表每个 ID 对应的完整 get_agent_status.snapshot，不能漏掉任何 ID。

host 先核验真实传输查询完整性与时间窗；helper 校验 sinceHours 覆盖 create 意图、列表数量
严格小于 limit、列表与 snapshots 的 ID/cwd/labels 对应，再排除历史 ID，按所有身份字段过滤。
当前已核验 MCP list_agents 没有分页 cursor；数量达到 limit 就无法证明完整，必须 WAIT_USER，
不能人工删减列表后声明零匹配。脚本本身不调用列表。缺字段、截断、非零匹配、错误过滤、
陈旧证据均拒绝。审计原字节及每次 profiles/创建尝试独立保留，最多两次创建意图。
prepared/confirmed_absent 且无 ID 的成员是计划，不伪造归档；新 stage 前所有真实 child 仍须
确认归档，歧义 dispatching 仍阻断。部分旧 stage 永远不能发布，后继完整 stage 保留所有历史。

首次 live 绑定保留完整 `snapshot.persistence` 与 `runtimeInfo`，可从 journal 读取该 child
的 provider/session 定位信息；这里不读取 provider 目录：

```bash
python3 -B - children.json "$KEY" <<'PYCODE'
import json, sys
rows = json.load(open(sys.argv[1], encoding='utf-8'))
row, = [r for r in rows if r['task_id'] + '|' + r['dispatch_id'] == sys.argv[2]]
s = row['first_live_capture']['snapshot']
print(json.dumps({k: s.get(k) for k in ('provider', 'cwd', 'persistence')}, ensure_ascii=False))
PYCODE
```

如果首个 live 尚无 session，保持首次观测原样，在首次 finish 通知后捕获完整 `terminal.json`，
从其 `snapshot.persistence.sessionId` 取得 session。宿主用该 session 的已知会话日志路径
显式设置 `NATIVE_LOG`：Codex 日志是会话日期目录内带 session ID 的 rollout JSONL，Claude
日志是项目会话目录内以 session ID 命名的 JSONL。目录根由运行环境提供，不能把另一安装的路径
或 ID 写进脚本；路径不明就补充该 child 的路径，不扫描所有会话或用 prompt 搜索其他日志。
parser 始终只打开 `--native-log` 指定的一个普通文件。session/cwd/prompt 的核验由内容完成，
文件名本身不是身份凭证。

仅在 finish 通知到达后重新取得终态事实，在归档前执行：

```bash
# NATIVE_LOG 是宿主明确定位的该 session 普通文件；所有输出路径均在本任务 ignored 目录。
python3 -B tools/orchestration/review_lifecycle.py native-export children.json "$KEY" \
  --capture terminal.json --native-log "$NATIVE_LOG" --outdir native-export --notified
# 成功后为 native-export/<task>/<dispatch>/terminal.raw 与 provenance.json；此时尚未审核通过。
# 也可直接导出并执行严格 harvest，一次命令完成这两步：
python3 -B tools/orchestration/review_lifecycle.py harvest children.json "$KEY" \
  --capture terminal.json --native-log "$NATIVE_LOG" --outdir raw-diagnostics --notified
# 若使用上一步已经导出的原始文件，兼容原有严格文件入口：
python3 -B tools/orchestration/review_lifecycle.py harvest children.json "$KEY" \
  --capture terminal.json --raw "native-export/$TASK/$DISPATCH/terminal.raw" --outdir raw-diagnostics --notified
```

只支持已实际核验的 **Codex 0.153.0** 与 **Claude Code 2.1.259** 结构。入口先核对已登记
STATE/journal direct child、通知、完整终态、root/workspace/parent/role/purpose/labels、首次
provider/session 和冻结创建 prompt SHA；同层与 persistence/runtimeInfo/metadata 的身份冲突拒绝。
新 create intent 保存 prompt SHA；缺少该冻结字段的旧 journal 不自动补写，应走纯解析审计。

Codex 要求单个 task_started/turn_context、连续 ordinal、明确 `phase=final_answer` 的单个
output_text，以及文件末尾同 turn_id 且字符串相等的 task_complete。已核验的环境 bootstrap
只能在创建 prompt 之前。Claude 要求唯一初始 prompt、完整 UUID/父链、单个最终 text block、
`stop_reason=end_turn` 和末尾 `last-prompt.leafUuid`；同 message 的 thinking block 不作为结果。
其他版本、未知结构、后续用户轮次、缺失/多义 final、截断、无末行换行、重复 JSON 键均拒绝。
最多读16MiB/10000行，打开前后及解析后核对普通文件身份、大小和时间，拒绝读取中的替换或增长。

输出直接编码原始字符串的 UTF-8 bytes，不 trim、不补换行、不删除分隔符、不重序列化模型 JSON。
最小 provenance 记录源路径/文件 SHA、版本/session、关键行与消息/turn ID、prompt SHA、raw SHA、
child/输入绑定，以及完整首个 live/终态捕获对象的 canonical SHA。不会复制完整会话或 thinking。
MCP curated 内容与 native 相等只说明某个样本；不能从 curated 内容普遍还原原文。已移除始终
UNPROVEN 的 SDK 诊断支线及 Node 依赖；其公开 API 的来源限制仍见[效率报告](../../docs/review-efficiency-20260912.md)。

来源失败保存 `error-N.json` 与 journal 的 terminal_fetch_errors，不设置 output_valid、不消耗
归档预算。补齐同 child 的有效来源后可重试；也可用下述带 capture 的 reject 核验终态后显式放弃。
已导出的 provenance/raw 不可覆盖；已完成判废或人工 reject 不因重导出而重新接受。
如仅 strict 验证中断，使用已保存 raw 的 `harvest --raw` 重验，保持相同 capture 和输出目录。

历史已归档样本只读验收使用 Python 纯接口，不调用生产 export/harvest：
`parse_native_final(data, provider=..., session_id=..., cwd=..., prompt=...)` 无 IO；
`read_native_final(path, **相同绑定)` 只读一个显式稳定文件。均返回 `(raw_bytes, provenance)`，
不访问 journal/STATE、不改历史 raw；调用方先独立核验冻结创建意图与终态身份再传绑定。

raw 先原样写入 `raw-diagnostics/<task>/<dispatch>.raw`，然后调用现有
`surface_screen_result_check.validate_result_bytes` 或 `contextual_result_check.validate_result_bytes`。
raw 保存后记 `validation_state=pending`；中断后重验已保存 bytes，不重新取输出。
真正结束的 validator 结果记 completed；人工 reject 记 rejected，二者均不会因重复 harvest 重新接受。
无效输出退出1、保留 bytes 和原因；它也必须归档。通知不是审核通过证明：ORCHESTRATOR
仍核对工作树、activity 和冻结读取边界。有实证违约时可判废已经通过 strict JSON 的结果：

```bash
python3 -B tools/orchestration/review_lifecycle.py reject children.json "$KEY" \
  --reason '具体违规事实' --evidence scope-audit.json
```

上述不传 capture 的用法要求 journal 已保存 terminal_capture。若已绑定的 child 收到完整
`status=error`／`attentionReason=error`／`activeTurn=null` 终态通知，却没有原生 session、
日志或 final，可以直接显式拒绝，无需先导出终稿：

```bash
# error-terminal.json 为该 direct child 的完整终态 status capture；error-audit.json 保存具体失败证据。
python3 -B tools/orchestration/review_lifecycle.py reject children.json "$KEY" \
  --capture error-terminal.json --notified \
  --reason 'provider 运行已报错结束，未产生终稿；详见失败证据' --evidence error-audit.json
# 成功后按下方 archive-intent → 外部归档 → archive-confirm 顺序执行。
```

带 capture 的拒绝先核验通知、首次 live 绑定、row／STATE／root／workspace／direct parent／labels、
冻结输入和完整终态，再保存不可覆盖的捕获与拒绝证据，记 `rejected`、`output_valid=false`。
同样的拒绝可重复执行；冲突捕获或证据拒绝写入。此动作不创建 raw，也不自动归档。
未拿到 raw 本身只是来源不可用；host 根据具体证据显式判废后才能归档并 fresh retry。
已有 raw 的输出判废保留原始 bytes；错误终态或通知本身都不构成有效 review。
原生导出仍只接受成功自然完成（idle／finished），不能用空 raw 或虚构原生日志绕过。

通知批量收获仍可使用 `harvest_reviews.py children.json rawdir --captures captures.json --notified`
（contextual 加 `--key verdicts`）。captures 是本地映射
`{"task|dispatch":{"terminal_path":"terminal.json","raw_path":"terminal.raw"}}`，
仅列出已经通知的成员。一个非法结果不影响其他已通知成员的 raw 留档；没有后台轮询或等待。

```bash
# 动作前重新查询并保存 status，再持久化预算。
python3 -B tools/orchestration/review_lifecycle.py archive-intent children.json "$KEY" --capture before-archive.json
# 仅退出 0 时调用一次 MCP archive_agent；退出 3 表示回读已归档，不再调用。
# archive 调用即使报错也重新查询，用独立 get_agent_status 回读结果确认：
python3 -B tools/orchestration/review_lifecycle.py archive-confirm children.json "$KEY" --capture archived.json
```

每次外部 archive 前，journal 和 STATE 都已原子保存递增预算；最多 2 次。
中断后先只读查询：已归档直接确认，尚未归档且预算仅 1 才允许最后一次尝试。
第二次预算消耗后未确认则保持 WAIT_USER/archive_pending；不能建 successor。
恢复点写在 `wait.resume_state`，重复 save 保留首次阶段；回读确认后从同处恢复，不自动发布完成记录。
save 跳过 DONE/STOP 的 STATE 字节重写。

归档全部完成后，失败 contextual full 用更高 `attempt`、新 `dispatch_id`、
`retry_of="task|old-dispatch"` 重新准备，candidate/input 路径及 bytes 必须完全相同。
surface 四 lane 必须重新生成完整新 attempt/group/manifest/dispatch，保持 workset，
不能只重派失败 lane。旧 child、raw、失败原因全部保留。helper 不负责重新生成 manifest，
继续使用现有 manifest 工具及冻结/preflight 步骤。

```bash
# spec 只选择成功的当前完整 stage，children 继续保留所有失败 attempt。
python3 -B tools/orchestration/close_review_tasks.py surface plan.json children.json rawdir
# 或 contextual ctx.json ctx-children.json ctx-rawdir
```

close 先重验完整 stage 与所有真实 child 的归档，并在原 workspace 检查输入/输出普通文件、
目录与路径；临时复制保留 symlink 拒绝条件。在临时工作空间用真实 `ai_state_check.check_state`
验证 prospective STATE，通过才写 raw／review records，最后原子发布 STATE 完成指针。
无效、partial、混组、旧 attempt、消费者拒绝均不发布新的接受记录。
中断在文件发布期间时，尚无完整 STATE 指针；重跑按 exact bytes 幂等恢复。
成功后 `rawdir/<dispatch>.json` 可交给原来的 `build_import_index.py`。
原生产 import／evidence／queue／DONE_VERIFIED 消费者照常运行，不能用 journal 替代它们。

## 分项计时与 fake transport

```bash
python3 -B tools/orchestration/review_lifecycle.py timing children.json > timing.json
```

记录模型窗口（首次 activeTurn.startedAt 至终态 attentionTimestamp）、收获验证、
归档意图至确认、准备至 create 意图和终态至收获间隔。没有端点就报告未测，不猜模型起止。
`Journal.timed(row, category, operation)` 是外部工具调用的可复用计时接口；
`harvest_and_archive(key, transport, outdir, notified=True)` 对注入 transport 的 status、
terminal_bytes、archive 调用自动计时，archive 错误后仍回读。取 raw 传输失败时保存
`terminal_fetch_errors` 历史，返回 None，不设置 output_valid、不归档；下一次显式调用可恢复。
确需放弃时，host 用 reject 提交具体原因/证据后才归档。fake transport 覆盖该路径。
适配器的 `status(key)` 须返回上述完整 MCP status 对象，`terminal_bytes(key)` 必须返回 bytes，
`archive(key)` 只执行一次动作。helper 不提供未核验的 CLI wire 适配器。

报告按类别计算时间区间的**并集**，并行模型时段不累加成墙钟；不同类别可能重叠，不能再相加。
MCP 手动调用的耗时只有调用者使用上述计时接口包裹时才有 tool_call 分项。
本次 fixture 只证明行为与计时口径，不预报固定节省秒数。

## 其余现有辅助工具

`freeze_workset.py`、`stage_surface.py`、`stage_contextual.py`、`build_import_index.py`
仍承担原有职责；源码输入配置见 [工具文档](../../i18n/README.md)。正式操作步骤见
[原 runbook](../../docs/baseline-batch-runbook-2026-09-06.md)，其中旧 harvest/CLI 示例以本文限制为准。
旧 `dispatch_reviewers.py`、`harvest_reviewers.py`、`harvest_contextual.py` 不用于新批次。

`run_batch_steps.py` 的两条已有串联保持：有 ISSUE 时 `surface-import=<index> contextual-export`，
以及 `adjudicate=<decisions> prepare-evidence`。各动作仍各自验证输入、锁、checkpoint 和事务，
同一 root/HEAD 的投影可复用；HEAD 改变重新投影。无 ISSUE 只运行 surface-import。
queue check/rebuild/status、batch start/finalize/recover、migration 不可串联；本次未扩充白名单。
