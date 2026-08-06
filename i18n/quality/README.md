# i18n/quality — 翻译质量系统权威规则

本目录是翻译质量系统（见 `docs/translation-quality-system.md` 与
`docs/translation-quality-phase-1.md`）的**权威配置**，进入版本控制；
任何规则、schema 或基准集的破坏性变更都必须提升 contract 版本，
不得原地重解释历史数据。

## 内容

| 文件 | contract | 说明 |
|---|---|---|
| `taxonomy-v1.json` | `tome4-quality-taxonomy-v1` | 文本 profile、severity、MQM 风格错误码、可合并错误码、门禁、置信度、等级、risk flag、profile 分类规则、长度桶 |
| `policy-v1.json` | `tome4-quality-policy-v1` | 身份契约、试点参数（seed/规模/桶/覆盖约束）、dry-run 参数、风险富集标志、质量向量维度、组件分组 |
| `rubric-v1.md` | `mqm-pilot-v1` | 评审指引：assessment 填写规则、错误码速查、severity 判定、评审纪律 |
| `../prompts/pi-quality-evaluator.md` | prompt SHA-256 | AI evaluator 的隔离、盲评、输出与逐条检查协议；由 `tools/pi-quality-evaluator` 与 rubric 合并后发送 |
| `schemas/inventory-v1.schema.json` | `tome4-quality-inventory-v1` | inventory.jsonl 条目契约 |
| `schemas/assessment-v1.schema.json` | `tome4-quality-assessment-v1` | 单评审者 assessment 契约 |
| `schemas/adjudication-v1.schema.json` | `tome4-quality-adjudication-v1` | 裁决契约 |
| `schemas/benchmark-v1.schema.json` | `tome4-quality-benchmark-v1` | 验收后不可变试点基准契约 |
| `policy-v2.json` / `rubric-v2.md` | `tome4-quality-policy-v2` / `mqm-pilot-v2` | v2 事实判定、数据隔离、span、匹配与裁决协议；不重解释 v1 |
| `impact-rules-v1.json` | `tome4-quality-impact-rules-v1` | 宿主确定性 severity 规则和固定优先级 |
| `anchors-v1.json` | `tome4-quality-anchors-v1` | 仅允许人工确认校准案例写入的版本化锚点；绑定 sample/revision/裁决并重算 severity |
| `stability-preregistration-v1.json` | `tome4-quality-stability-preregistration-v1` | 校准稳定性运行次数、模型、冻结 hash、失败语义和通过门槛 |
| `schemas/*-v2.schema.json` / `schemas/issue-cluster-v1.schema.json` / `schemas/dispute*-v1.schema.json` | 对应 `$id` | v2 assessment、问题簇、匿名争议、身份映射、事实裁决、稳定性和报告契约 |

## 边界

- 全量 inventory、抽样中间文件、评审原始输出和报告都是**派生 artifact**，
  只写入 `.artifacts/i18n/quality/runs/`，不进入版本控制。
- 未经裁决的模型输出不得进入本目录。
- 试点裁决通过验收并获得明确批准后，才把
  `benchmarks/pilot-v1.jsonl` 加入版本控制。
- 本目录文件由 `tools/i18n quality` 命令读取；运行前
  `python3 -B tools/i18n doctor` 检查工具链。
- `tools/pi-quality-evaluator` 可把一个有界 sample 交给单个无工具、无会话的
  Pi 模型盲评；宿主固定 evaluator 元数据并用本目录规则严格验证完整覆盖。
  evaluator 不接收另一评审者结果、裁决、历史 finding 或预期 grade；外部传输
  必须先按 `AGENTS.md` 获得授权。
- `quality stability-v2` 只接受同一 evaluator 的两份完整 assessment 和两份
  独立非缓存 runner report；逐字节相同的 assessment 合法，但复用同一报告或
  cache hit 不得冒充第二次稳定性运行。

## 身份约定

- `unit_id`：复用 `stable_entry_id`（component/section/source/source_tag 的
  SHA-256 editorial key）。
- `revision_id`：对 `{identity_contract, version, unit_id, target,
  args_order, special}` 的规范 JSON（UTF-8、键排序、无多余空白）取 SHA-256；
  行号和 ordinal 不参与身份。
