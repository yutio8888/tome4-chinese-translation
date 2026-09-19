# Token efficiency：2026-09-19 有界首轮实现

本轮只减少重复交接文本和 routine host 回显，并增加离线用量比较入口。它不改变审核人数、
provider 策略、生命周期 backend、证据身份或语义裁决，也不恢复当前暂停的生产批次。

## 本地字节测量

这些是 UTF-8/JSON **输出字节数**，不是 tokenizer 结果、token 节省、费用或生产速度结论。

在本候选工作树运行：

```bash
git show c2b03ac91195ad5a0a6016c4166bf7659109092b:handoff.md | wc -c
wc -c handoff.md
```

结果为旧交接 `101711` bytes、当前交接 `3571` bytes，减少 `98140` bytes（约 96.49%）。
旧正文已移入 `docs/handoff-history-through-20260919.md`；迁移只加存档声明并修复相对链接，
历史正文不再作为当前授权载入。

下列命令对同一个代表性四行 `host-event` state 同时序列化完整值和 compact 值：

```bash
node -e 'const {compactReviewHostState:c}=require("./tools/orchestration/review_host.js"); const rows=[1,2,3,4].map((n,i)=>({key:`task|lane-${n}`,agent_id:i<3?`agent-${n}`:null,status:i<3?"dispatched":"prepared",archive_confirmed:false,archive_attempts_started:0,validation_state:null,live_bound:i<3,create_blocked:false})); const state={rows}; const cfg={children:".artifacts/i18n/task/children.json",outdir:".artifacts/i18n/task/host",nativeLogs:{}}; const compact=c(state,{type:"fill"},cfg); console.log(JSON.stringify({full_bytes:Buffer.byteLength(JSON.stringify(state)),compact_bytes:Buffer.byteLength(JSON.stringify(compact))}));'
```

结果为完整值 `744` bytes、compact 值 `406` bytes。routine summary 聚合状态，只保留 finish
通知需要的未归档 `key`/`agent_id` 和权威 journal/outdir 指针；只有可操作异常才展开逐行 recovery，
只有失败才带 errors。`reviewHostDetailed` 仍可把同一未截断 state 交给代码，journal、wire、raw 和
provenance 从未截断。这一小型 fixture 只证明该输入的序列化字节差，不承诺端到端 token 或墙钟收益。

## 显式用量记录 schema

`tools/orchestration/review_usage.py` 只读取命令行明确给出的一个普通 JSON 文件，最多 8 MiB、
10000 条；拒绝 symlink、特殊文件、重复 JSON key 和重复 `request_id`。它不发现或扫描 native
session，不调用 provider，不写输入、任务状态或 production evidence，报告仅写 stdout：

```bash
python3 -B tools/orchestration/review_usage.py explicit-records.json > local-report.json
```

输入顶层必须且只能有：

```json
{
  "schema": "review-usage-records/1",
  "records": [
    {
      "request_id": "batch-211/surface/lane-1/request-1",
      "role": "CHILD",
      "batch": "batch-211",
      "phase": "surface",
      "counter_scope": "request",
      "usage": {
        "input_tokens": 1200,
        "cached_input": {"tokens": 400, "relationship": "subset_of_input"},
        "output_tokens": 180
      },
      "interval": {
        "started_at": "2026-09-20T01:00:00Z",
        "ended_at": "2026-09-20T01:01:00Z"
      }
    }
  ]
}
```

每条 record 必须且只能含示例中的七个字段：

- `request_id` 是调用方提供的全文件唯一请求身份；重复即拒绝，不猜测去重。
- `role` 只能是 `ORCHESTRATOR` 或 `CHILD`。报告将所有 child 合为 `CHILDREN`，并同时按
  `batch`/`phase` 分组；三个字段都必须是非空字符串。
- `counter_scope` 只能是 `request` 或 `last_usage_snapshot`。后者始终单独汇总并明确标为快照，
  **绝不称为 whole-session total**。
- `input_tokens` 和 `output_tokens` 是非负整数或 `null`。`null` 表示未知；未知不会变成实测 0。
- `cached_input` 为 `null`（未知），或包含非负整数 `tokens` 和 relationship。
  `subset_of_input` 表示 cached 是 `input_tokens` 的子集，可在两者都已知时计算
  `input_excluding_cached_subset_tokens`，且 cached 不得大于 input；`separately_measured` 表示独立
  计数，不能从 input 中相减。两类永远分栏汇总。
- `interval` 为 `null`（未测），或含两个带时区的 ISO-8601 端点。每组 `observed_span_ms` 是
  最早 start 到最晚 end 的观测跨度；重叠 child 不相加。它不自动等同完整 batch 墙钟，缺端点仍标未知。

脚本不计算价格、不估算 tokenizer token、不从 provider 名推断计数语义。来源系统没有提供的指标
保持 unknown；调用方必须按其真实计数口径选择 `counter_scope` 和 cached relationship。

## 未来授权批次的采集办法

生产当前仍暂停。维护者以后明确恢复批次时，可在不改变审核流程的前提下，由 ORCHESTRATOR 为
每次自身请求和每个 child 请求分配稳定 `request_id`，记录 provider 明确返回的 input/cached/output
计数及其真实口径，并在实际请求开始/结束处记录带时区端点。不要从聊天历史或 native session 反推，
不要把最后一次 `lastUsage` 当累计值。批次完成后把明确记录文件单独传给上述离线 CLI，比较相同
batch/phase 下的 ORCHESTRATOR 与 CHILDREN。

要声称生产收益，至少需要恢复后经授权的可比批次、相同流程边界、已知计数口径和明确 batch
墙钟端点；本实现没有这些数据，因此不声称已测得端到端 token、成本或速度改善。
