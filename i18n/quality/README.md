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
| `policy-v3.json` / `rubric-v3.md` | `tome4-quality-policy-v3` / `mqm-pilot-v3` | 低主观性 evaluator：模型只报告可观察语义差异，宿主确定性派生分类和 severity |
| `severity-matrix-v1.json` / `anchors-v2.json` | 对应 `contract` | v3 严格兼容矩阵、技术门禁优先级和六条人工 anchor 的无损投影 |
| `stability-preregistration-v2.json` / `schemas/*-v3.schema.json` | 对应 `$id` | v3 校准冻结身份、assessment、裁决、报告和 raw/normalized 稳定性契约 |
| `facts-study-v1.json`、`facts-study-v2.json` / `schemas/fact*.schema.json` | `tome4-quality-facts-study-*` | v1 保留失败 pilot；v2 使用 supplemental-only Fact packet，仍为 20 条、七 arm、33-slot 且永不产生 holdout clearance |
| `facts-study-v3.json` / `schemas/facts-study-*.v2/v3*.schema.json` | `tome4-quality-facts-study-protocol-v3` 等 | curation v1：80 条 source-side 候选池、quota 选择、受控变体边界、offline-frozen preregistration（外部 runner 拒绝执行） |
| `facts-study-v4.json` / `schemas/facts-study-protocol-v4.schema.json` | `tome4-quality-facts-study-protocol-v4` | 长文本富集池（≥300 字符带、long-source 优先、数字/条件风险加分、term/ui 配额缩减） |
| `facts-study-v5.json` / `schemas/facts-study-protocol-v5.schema.json` | `tome4-quality-facts-study-protocol-v5` | 语料对齐配额（fd 12 / surface 2，claim 级冻结门槛 8+8+5+3 不变）；select 选择 trap-优先 + 覆盖缺失 stratum |
| `dataset-registry-v1.json` / `schemas/dataset-registry-v1.schema.json` | `tome4-quality-dataset-registry-v1` | 版本化数据集登记（正式 120、32+32、探索集、失败 pilot、候选集）；工具只读，冻结只生成 registry fragment 由主代理合入 |
| `schemas/quality-common-v1.schema.json` | `tome4-quality-common-v1` | 公共 claim/evidence/provenance/fact/subject/uncertainty $defs，供 curation 与 v2 契约引用 |
| `language-channel-v1.json` | `tome4-quality-language-channel-v1` | 只冻结独立语言质量通道的输入、taxonomy 与 lineage 边界；本轮不授权或执行外部校准 |
| 正式报告 `docs/translation-quality-facts-study-report-v1.md` | — | 33-slot 外部因果研究最终报告（do-not-promote-facts-channel），归档索引 `.artifacts/i18n/quality/facts-study-campaign-archive.json` |

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
- 盲评模型 finding 只接受 `is_defect=yes` 且 `is_substantive=yes` 的实质缺陷。
  纯 presentation/style、可选润色和 `presentation-only` 不属于模型 finding；
  确定性排版/结构问题由宿主 gate 负责，presentation minor/note 规则只供宿主
  或人工裁决使用。模型 technical finding 还必须有 bundle 内 gate 确认。
- `quality stability-v2` 只接受同一 evaluator 的两份完整 assessment 和两份
  独立非缓存 runner report；逐字节相同的 assessment 合法，但复用同一报告或
  cache hit 不得冒充第二次稳定性运行。
- v3 使用显式版本命令：`calibration-v3`、`evaluator-bundles-v3`、`match-v3`、
  `disputes-v3`、`adjudicate-v3`、`report-v3`、`stability-v3`。v1/v2 命令和
  artifact 原义不变；`tools/pi-quality-evaluator` 按 sample contract 自动分派。
- v3 固定 20 条/shard（32 条恒为两个 shard）。校准 runner 必须给出 preregistration、
  `--run-number 1|2` 并关闭缓存；原子 campaign ledger 最多消费 8 个槽，失败不重试、
  不替换；单次 assessment 完整通过严格校验后，相关 shard 才会一起标记成功。
  preregistration 同时冻结 bundle ID 与完整 bundle hash，ledger 逐槽核对实际
  shard/bundle 身份。`stability-v3` 只把每位 evaluator 的通过报告 ID 原子登记到
  同一 ledger，且不同报告不得替换。holdout 在 provider 调用前要求 8 个槽全部成功，
  并要求同一 preregistration 下已登记的 reviewer-a/b 两份通过报告；缓存身份绑定
  该 clearance。
- v3 bundle 不向模型展示 anchor 或 severity。负 anchor 仅拒绝同 revision、同规范化
  证据范围、同分类的已知伪 finding；正 anchor 仅规范化已检出的同范围 finding，
  不会向 clean item 注入 finding。封存集和正式集不应用精确 anchor。
- `report-v3` 绑定 adjudication validation ID（无裁决为 null），读取时按 match 与裁决
  重新派生全部指标；JSON Schema 无法表达的跨 artifact 关系由宿主重验。
- Facts 研究最新数据契约为 `facts-study-v2`：Fact packet 只允许真正新增的 supplemental
  信息，每项可为 0–4 条，公共 source/context 重述被禁止；v1 失败 pilot 保留并自动进入
  历史排除集。命令使用 `facts-study-build`、`facts-study-bundles`、`facts-study-validate`、
  `facts-study-report` 和独立 runner `tools/pi-quality-facts-study`。draft gold、缺少双人
  review/adjudication lineage 或不满足 8+8 claim、5 clean、3 fact-trap 配额时，宿主
  拒绝生成外部可执行 preregistration。缓存关闭，失败 slot 不补跑、不替换。
- `facts-study-curation-*` 是 curation v1 数据流：`facts-study-curation-build` 生成
  80 条 source-side 候选池（选择只读 source/source tag/section/profile/公开上下文/术语
  特征，任意替换 target 不改变选择）；`facts-study-curation-prepare` 在 Facts 冻结后
  生成 target-visible curator bundle；`facts-study-curation-select` 按 curator
  assessment 选择最终 20 条（8 fact-dependent、6 surface、6 clean/acceptable，其中
  ≥5 clean、≥3 fact traps），natural 优先，不足时退出码 2 并产出受控变体 request，
  受控仅补 fact-dependent 缺口且不授予 clearance。`facts-study-bundles/validate/report`
  按 sample/prereg contract 自动分派 v1/v2；v2 preregistration 固定
  `status=offline-frozen`，外部 runner 与外部 assessment 一律拒绝，fake replay 的
  report 固定为 `non-evidentiary-offline-replay` 且 natural/controlled 指标分离。
  Facts statement 统一使用英文元语言。
- 共享 claim/contract 核心位于 `tools/i18nlib/quality_contracts.py` 与
  `tools/i18nlib/quality_claims.py`；v2/v3/Facts 旧模块保留原导出名，通过 re-export
  调用公共实现，历史 contract/artifact 不变。

## 身份约定

- `unit_id`：复用 `stable_entry_id`（component/section/source/source_tag 的
  SHA-256 editorial key）。
- `revision_id`：对 `{identity_contract, version, unit_id, target,
  args_order, special}` 的规范 JSON（UTF-8、键排序、无多余空白）取 SHA-256；
  行号和 ordinal 不参与身份。
