# i18n/quality — 翻译质量系统权威规则

本目录是翻译质量系统（见 `docs/translation-quality-system.md` 与
`docs/translation-quality-phase-1.md`）的**权威配置**，进入版本控制；
任何规则、schema 或基准集的破坏性变更都必须提升 contract 版本，
不得原地重解释历史数据。

## 内容

| 文件 | contract | 说明 |
|---|---|---|
| `taxonomy-v1.json` | `tome4-quality-taxonomy-v1` | 文本 profile、severity、MQM 风格错误码、可合并错误码、门禁、置信度、等级、risk flag、profile 分类规则、长度桶 |
| `policy-v1.json` | `tome4-quality-policy-v1` | 身份契约、试点参数（seed/规模/桶/覆盖约束）、风险富集标志、质量向量维度、组件分组 |
| `schemas/inventory-v1.schema.json` | `tome4-quality-inventory-v1` | inventory.jsonl 条目契约 |
| `schemas/assessment-v1.schema.json` | `tome4-quality-assessment-v1` | 单评审者 assessment 契约 |
| `schemas/adjudication-v1.schema.json` | `tome4-quality-adjudication-v1` | 裁决契约 |
| `schemas/benchmark-v1.schema.json` | `tome4-quality-benchmark-v1` | 验收后不可变试点基准契约 |

## 边界

- 全量 inventory、抽样中间文件、评审原始输出和报告都是**派生 artifact**，
  只写入 `.artifacts/i18n/quality/runs/`，不进入版本控制。
- 未经裁决的模型输出不得进入本目录。
- 试点裁决通过验收并获得明确批准后，才把
  `benchmarks/pilot-v1.jsonl` 加入版本控制。
- 本目录文件由 `tools/i18n quality` 命令读取；运行前
  `python3 -B tools/i18n doctor` 检查工具链。

## 身份约定

- `unit_id`：复用 `stable_entry_id`（component/section/source/source_tag 的
  SHA-256 editorial key）。
- `revision_id`：对 `{identity_contract, version, unit_id, target,
  args_order, special}` 的规范 JSON（UTF-8、键排序、无多余空白）取 SHA-256；
  行号和 ordinal 不参与身份。
