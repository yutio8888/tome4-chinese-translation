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
`stop_reason=end_turn` 与唯一最终链；默认历史模式另要求末尾 `last-prompt.leafUuid`，
生产成功自然终态模式详见下方 P1 配方。同 message 的 thinking block 不作为结果。
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
## MCP 宿主 stdin 配方（P1）

以下 `functions.exec` JavaScript 定义 `reviewHost`，同一段代码由测试从本文提取执行。
在同一个 exec 中追加调用，或重新定义函数后按 journal 恢复。`cfg` 指向已冻结并 prepared 的有限
stage：`children`、`outdir`、`keys`（有序 key 列表）、`profileIds`（key → 已按 notes 选定的 ID）、
`nativeLogs`（key → 明确原生日志路径）。每次创建仍实时读取 profiles；冻结 selection 的 provider/model 须与 profile 一致。
可选 modeId、thinkingOptionId、featureValues 逐来源验证类型：仅一方声明时使用该值，双方声明时必须一致，
双方缺失时不传。null 或非法类型不视为缺失。映射结果保存在本次 intent，不从标题推断或补填运行时身份。
生产使用仓库 cwd 和默认 helper；`cfg.helper` 仅供隔离 fixture 指向同一脚本绝对路径。
Python 只消费 stdin，不能调用宿主注入的异步 MCP tools。每次工具调用的完整返回及计时都经 shell
单引号转义保存；`JSON.stringify` 只负责 JSON 编码，不能代替 shell quoting。

```javascript
// BEGIN REVIEW_HOST_RECIPE
async function reviewHost(tools, cfg, action) {
  const quote = s => "'" + String(s).replace(/'/g, "'\\''") + "'";
  const helper = cfg.helper || 'tools/orchestration/review_lifecycle.py';
  async function event(key, op, extra = {}) {
    const input = JSON.stringify({op, ...extra});
    const args = ['python3', '-B', helper, 'host-event', cfg.children, key, '--outdir', cfg.outdir];
    if (cfg.nativeLogs[key]) args.push('--native-log', cfg.nativeLogs[key]);
    const reply = await tools.exec_command({
      cmd: "printf '%s' " + quote(input) + ' | ' + args.map(quote).join(' '),
      yield_time_ms: 1000, max_output_tokens: 4000
    });
    // A still-running local command must be resumed by the host; never repeat it.
    if (reply.session_id) throw new Error('Local command running; resume session ' + reply.session_id);
    if (reply.exit_code !== 0) throw new Error(reply.output || 'host-event failed');
    return JSON.parse(reply.output);
  }
  async function call(key, op, fn, extra = {}) {
    const started_at = new Date().toISOString();
    let response;
    try { response = await fn(); } catch (error) {
      await event(key, 'call-failed', {operation: op, started_at, ended_at: new Date().toISOString()});
      throw error;
    }
    return event(key, op, {...extra, response, started_at, ended_at: new Date().toISOString()});
  }
  let state = await event(cfg.keys[0], 'recover');
  const row = key => {
    const hits = state.rows.filter(r => r.key === key);
    if (hits.length !== 1) throw new Error('Unknown dispatch');
    return hits[0];
  };
  async function fill() {
    for (const key of cfg.keys) {
      if (state.rows.some(r => r.status === 'dispatching'))
        throw new Error('Ambiguous create: reconcile before any create');
      for (const r of state.rows.filter(r => r.status === 'created')) {
        state = await call(r.key, 'bind', () => tools.mcp__paseo__get_agent_status({agentId: r.agent_id}));
      }
      if (state.rows.some(r => r.create_blocked)) return;
      const occupied = state.rows.filter(r => r.agent_id ? !r.archive_confirmed :
        !['prepared', 'confirmed_absent'].includes(r.status)).length;
      if (occupied >= 3) return;
      if (!['prepared', 'confirmed_absent'].includes(row(key).status)) continue;
      state = await call(key, 'profiles', () => tools.mcp__paseo__list_profiles({}),
                         {profile_id: cfg.profileIds[key]});
      // Intent is durable. A lost create response leaves dispatching; no automatic retry.
      state = await call(key, 'create', () => tools.mcp__paseo__create_agent(state.parameters));
      const agentId = row(key).agent_id; // ID persisted by Python before the first status call.
      state = await call(key, 'bind', () => tools.mcp__paseo__get_agent_status({agentId}));
    }
  }
  if (action.type === 'fill') {
    await fill();
  } else if (action.type === 'finish' || action.type === 'recover-archive') {
    const key = action.key;
    const r = row(key);
    if (r.agent_id !== action.agentId) throw new Error('Notification agent/dispatch mismatch');
    if (r.archive_confirmed) return state; // Duplicate notification: no remote action.
    if (!r.live_bound) throw new Error('Recover first live binding before processing notification');
    if (action.type === 'recover-archive' && !['completed', 'rejected'].includes(r.validation_state))
      throw new Error('Incomplete harvest requires original notification evidence');
    if (!['completed', 'rejected'].includes(r.validation_state)) {
      state = await call(key, 'harvest', () => tools.mcp__paseo__get_agent_status({agentId: r.agent_id}),
                         {notified: true, notification_received_at: action.receivedAt || null});
    }
    // Always read back first, including recovery after a lost archive response/readback.
    state = await call(key, 'archive-intent', () => tools.mcp__paseo__get_agent_status({agentId: r.agent_id}));
    if (state.archive) {
      try {
        state = await call(key, 'archive-response', () => tools.mcp__paseo__archive_agent({agentId: r.agent_id}));
      } finally {
        state = await call(key, 'archive-confirm', () => tools.mcp__paseo__get_agent_status({agentId: r.agent_id}));
      }
    }
    await fill(); // First released slot starts member 4 before touching members 2/3.
  } else {
    throw new Error('Unknown host action');
  }
  return state;
}
// END REVIEW_HOST_RECIPE
```

初始执行 `text(await reviewHost(tools, cfg, {type: 'fill'}));`；收到已知 child 的真实 finish 通知后，
调用 `text(await reviewHost(tools, cfg, {type: 'finish', key, agentId, receivedAt}));`，
`receivedAt` 为实际收到通知时记录的 ISO 时间；若此前未记录可省略并标未测量。未收到通知时继续其他工作，
没有定时轮询、sleep 或 idle 猜测取消。一个 journal 只能由一个宿主串行调用。
归档回读丢失后使用 `{type: 'recover-archive', key, agentId}`，先回读，已关闭直接确认；否则只使用
剩余预算。两次耗尽进入原 WAIT_USER 语义；该成员后续仅确认状态，其他已有成员仍可首绑定、取证及使用剩余预算归档。
共享 create_intent 在落意图前拒绝 DONE/STOP/WAIT_USER 和未解决的耗尽归档，fill 同步停止新建，
即使另一成员释放名额也不派发。保留预算 2 与 wait.resume_state，按原恢复条件确认已有成员后才恢复 fill。
archive 异常仍回读；若 finally
已确认而原异常仍抛出，重载后 `fill` 可立即释放名额。create 返回丢失须按既有 reconciliation
契约查证：唯一完整捕获用 bind，确定不存在用 reconcile-absent；不得再调用 create 猜测。
本配方不做列表发现，也不提供自动停止/取消。

`host-event children.json 'task|dispatch' --outdir ...` 的 stdin 为
`{op, response, started_at, ended_at}`；profiles 另带 `profile_id`，harvest 另带真实通知的
`notified: true` 与可选实际 `notification_received_at`。传输抛错另存无响应的 `call-failed`，
记录 operation 与起止，不虚构 response。完整外壳保存到 `outdir/task/dispatch/wire/<sha>.json`；未知结构、isError、重复键、
多文本块及两份 payload 冲突均拒绝。仅支持已核验的 count/ids 前缀＋JSON，以及直接 JSON 文本；
不会对人读前缀盲目 json.loads，也不会忽略前缀后与 structuredContent 冲突的 JSON。
错误终态停在 harvest，需宿主以真实证据执行上述 explicit reject 后再归档；`--raw` 不能接受错误终态。

Claude 2.1.259 的纯 parser 默认仍要求 last-prompt；显式 `natural_success=True` 支持最终 assistant
结束、真实 last-prompt、以及其后一个 `{type, aiTitle, sessionId}`。生产仅在完整成功终态和
首次 live/STATE 身份核验后启用。missing/null 可选 session 别名表示未知，非空已知值必须一致。
proof 保留完整 source SHA、原样 raw SHA、final 位置与尾部形态；不会补写 last-prompt。
已冻结的 raw/proof 在归档前可幂等复用，来源缺失或变化可恢复，显式判废不复活。

`timing` 另输出 createdAt spread、成员终态/通知时间、stage 墙钟与已记录工具调用数；
null 端点为未测量。`model_window` 是 activeTurn 窗口，**包括工具时间**，不是纯模型时间。
README fixture 验证顺序与故障，不代表真实 stage 吞吐实测。真实 MCP 返回卸壳的只读复算与
生产端到端、实际省时是三类不同证据，详见[本任务报告](../../docs/review-speed-p1-20260912.md)。

## 可选源码事实输入（P1-C）

首次冻结 contextual 候选时，可把当前 `freeze_workset.py` 元数据齐备的已有 selected
源码工作集交给真实 CLI（包含 `source_pinning`、`fixed_source_commit` 等绑定字段；
缺失即明确失败，不为旧工作集补默认身份）：

```bash
python3 -B tools/i18n production batch contextual-export \
  --source-workset evidence/quality/production-batches/<batch>-source-workset.json
```

同进程组合保留 surface-import 的结果和投影复用；无需为筛选 deep 条目另跑查询：

```bash
python3 -B tools/orchestration/run_batch_steps.py \
  surface-import=/tmp/surface-index.json \
  contextual-export=evidence/quality/production-batches/<batch>-source-workset.json
```

裸 `contextual-export` 与原七字段 envelope、candidate 计算保持兼容。新入口在 writer lock
和既有 preflight 后读取一次普通工作集，核对全部 selected 的 batch/catalog/base、冻结行与
verification 绑定，再仅为 deep_required 构建事实。全部 run 验证完成后才写入；错误不回退为裸导出。
工作集原始 bytes SHA、manifest 摘要、run 有序成员和源码／术语事实经包 SHA 绑定到 context。
SHA 不放 briefing；新增 JSON 中的等号编码为 `\u003d`，JSON 解码可还原，原 args_order 前缀保留。

来源配置沿 `i18n/versions/tome-1.7.6.json`：固定来源使用 `TOME_ENGINE_ROOT` 等仓库配置，
按 manifest commit 读取 Git 普通 blob；extractor 使用其独立固定 commit。checkout 修改或删除
不会改变固定输入。DLC 使用 `TOME_DLC_ROOT` 下唯一匹配目录，或显式组件根
`TOME_DLC_CULTS_ROOT`、`TOME_DLC_ORCS_ROOT`、`TOME_DLC_ASHES_ROOT`；组件根中保留
`tome-cults/` 等 public path 前缀。多个目录匹配直接拒绝。DLC 公开源码版本未固定，提取快照
不是源码 commit；所有读入 bytes 均核对工作集 SHA。绝对 public path、`..`、symlink、
缺失文件、非法 UTF-8、错误 hash／行号均报错。

术语优先取 batch base commit，按生产 `terminology_snapshot` 的 path/length framing 核对；
当前文件只有同摘要才能替代。保留 scope/tag/status/notes，nil 与空串严格区分。事实只有有限
源码入口和格式标记，不复制工作集的 confirmed/rule 结论，不扫描其他译文的现有用法；
数量含义保持 unknown，无归属合法空命中标 pending。默认上下文 ±3 行，每条最多 8 入口、
120 展示行、32 KiB canonical 事实，每 run 最多 512 KiB；超限拒绝，不静默截断。

已有或请求带事实的候选只允许相同 bytes 幂等复用；变更事实、工作集排版或省略参数均不能
覆盖已冻结事实。需要变更时，先由宿主按既有 `production batch abandon`／重新 start、
surface-export/import 流程处理当前边界，再以新 checkpoint 绑定的工作集首次导出；
`recover` 用于修复当前状态，不自动授予覆盖候选权限。已冻结 import、prepare 和证据回放
消费 envelope 本身，不重新读取构建材料。原 `build_evidence_pack.py <batch> --context 3
--siblings 4` 入口仍可用，与新路径共享构建器；siblings 参数仅保留兼容，旧包不批量改写。
旧历史 envelope／replay 不新增源码或术语读取依赖。独立脚本独占创建 `.json.tmp`；
该临时路径预存时直接失败，保留输入和已有 pack，不跟随符号链接或覆盖临时文件。

验证与限制见 [P1-C 实现报告](../../docs/review-speed-p1c-20260912.md)。生产省时尚未测量；
fixture 中的投影次数和运行耗时不代表生产收益。

## Contextual 导入、裁决生成与证据准备（P2-B）

已完成 surface 导入和 contextual 导出、有真实 contextual 任务的 DONE_VERIFIED 与原始
结果后，可使用固定四步入口。先准备与当前 checkpoint 的 batch/catalog/base、selected
冻结行逐项一致的 source-workset，再由宿主准备决策说明；不得从模型 verdict 自动决定
confirmed。所有 ISSUE 观察各有一个键，同一 revision 的 surface/contextual 分开裁决。

在生产仓库 cwd 执行下面命令，替换三个准备材料路径和本次唯一的输出名：

```bash
python3 -B tools/orchestration/build_import_index.py contextual /tmp/contextual-raw /tmp/contextual-index.json
python3 -B tools/orchestration/run_batch_steps.py contextual-adjudication-chain \
  --input /tmp/contextual-index.json \
  --spec /tmp/adjudication-spec.json \
  --output .artifacts/i18n/adjudication-chain/batch-id-attempt-01.json \
  --source-root /path/to/public-source-root
```

`adjudication-spec.json` 示例（revision 前十位须替换为当前实际值，列齐全部观察）：

```json
{
  "workset": "evidence/quality/production-batches/batch-id-source-workset.json",
  "decisions": {
    "0123456789|surface": {
      "disposition": "confirmed",
      "repair_required": true,
      "conclusion": "宿主对公开源码与当前观察的具体裁决理由"
    },
    "0123456789|contextual": {
      "disposition": "advisory",
      "repair_required": false,
      "conclusion": "宿主对语境观察的具体裁决理由"
    }
  }
}
```

专用入口只执行 `contextual-import → generate → adjudicate → prepare-evidence`，
不接受任意动作串。三个生产动作仍经过真实 CLI，各自获取锁与验证 checkpoint/SQLite；
生成函数单独持有 writer lock，重新 preflight 后读取已接受 observations。唯一共享物是
同 root/HEAD 的 carry 投影，无外层锁、嵌套 scope、生成子进程或持久缓存。
root 与生产 CLI 一致：非空 `I18N_REPOSITORY_ROOT` 解析为绝对路径，未设置或空串均使用
脚本所属仓库；相对输入、workset、
source-root、output 路径仍相对当前 cwd。其他辅助脚本和旧生成 CLI 使用仓库 cwd，
不能仅用该环境变量代替切换 cwd。

导入前拒绝非普通 index/spec/workset、重复 JSON 键、非法类型和已占用输出。
spec/workset 使用本次一次读取的 bytes，随后磁盘修改不会替换本次宿主决策；index/raw
在导入前、生成前再次逐字节核对。当前 checkpoint 的完整 workset 绑定及观察集合只能在
导入后的生成 preflight 中核验，缺失／多余决策到此才拒绝。disposition 仅允许
confirmed/pending/advisory/refuted，repair_required 必须为 JSON bool，且仅 confirmed 可为 true。

源码只读取 confirmed 所需的 `public_source_path`：必须能由显式 source-root 表达，路径
相对、无穿越、无 symlink，并且普通文件原始 bytes 的 SHA256 等于工作集
`source_verification.source_file_sha256`。快照原样保存 UTF-8 与换行。
这证明**与工作集 SHA 一致**，不证明公开来源的 commit 或来源身份；DLC 来源未固定的事实
不会因此改变。不匹配、缺失或需要多个无法由该根表达的来源时拒绝，不回退 ENGINE。
此时可由宿主按现有十字段裁决规范准备文件，再独立调用 adjudicate。

输出必须是生产 root 的 `.artifacts/i18n/adjudication-chain/` 内 fresh 文件；普通文件、
目录和悬空 symlink 均算占用，所有父目录须普通。临时文件在目标目录独占创建，完整写入并
fsync 后以不覆盖目标的 hard-link 原子发布，再同步目录并删除自己的临时文件。
并发目标保留对方 bytes；失败可能留下本次创建的空目录，不清理其他文件。发布后异常也停止，
现有输出不作为成功重试信号。scratch 文件是中间输入，持久裁决仍由原 evidence 流程发布。

失败后以 checkpoint 为准，保留所有原始审核证据：

- 导入失败：修复对应 raw／DONE 绑定后，使用相同冻结材料重新执行。
- 导入成功、生成失败：修复宿主说明、来源或输出问题；可用 fresh 输出重跑该链，
  原 contextual-import 对相同结果仍按原消费者规则处理。不会重新使用旧裁决文件。
- 已生成、adjudicate 失败：核对文件和失败原因，按原规范修复／另存后独立执行下方 adjudicate。
- prepare 失败：保留 adjudicated，独立重跑 prepare，门禁重新执行。
- 发布后目录同步等错误：文件可能已存在，先核验该文件；独立消费者恢复，不能把文件存在当成功。

```bash
python3 -B tools/i18n production batch contextual-import --input /tmp/contextual-index.json
# 必要的手工裁决准备完成后；该文件也可为已核验的 scratch 输出：
python3 -B tools/i18n production batch adjudicate --input /tmp/validated-adjudications.json
python3 -B tools/i18n production batch prepare-evidence
```

旧 `make_adjudication.py <spec.json> <out.json>` 两位置入口仍合法，默认读取 ENGINE 当前
checkout，普通输出覆盖和摘要保持兼容；它不获得新链的 source-root/SHA/fresh 保障。
旧入口仍以当前 cwd 为 root，现在也会在 preflight 前获取 writer lock，可能在该 cwd 下
创建 `.artifacts/i18n/production-review-v2-lite/repository.lock` 及其父目录；其他 writer
占用锁时立即拒绝，尚未执行 preflight。应先切换到目标仓库 cwd。旧 baseline 的 preflight
本身就可能协调孤立 reservation／SQLite 状态，不能概括为纯只读；此处新增的是 writer lock
及对应的文件／目录创建和占用拒绝行为。
旧六动作 parse 和 `contextual-export=<workset>` 保持。纯 surface 无 ISSUE 走既有合法
空裁决 `adjudicate=<empty.json> prepare-evidence`，不制造 contextual 前置状态。
start/finalize/abandon/recover、queue 管理/check 与 migration 继续独立运行。

有界 fixture 实测两种有 contextual 任务的路径均从 3 次投影降至 1 次；生产秒数未测量，
不由 P2-A 106 秒样本推算批次收益。测试使用既有 gate seam，不能证明真实 17 门禁通过。
测试命令、错误时序、作者测试隔离事故与验收边界见 [P2-B 报告](../../docs/review-speed-p2b-20260912.md)。
