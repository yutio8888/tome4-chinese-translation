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
| 正式报告 `docs/translation-quality-facts-study-report-v1.md` | — | 33-slot 外部因果研究最终报告（do-not-promote-facts-channel）；长期 A-core 归档身份为 `ee8973e1…`，不进入源码仓库 |

## 边界

- 全量 inventory、抽样中间文件、评审原始输出和报告都是**派生 artifact**，
  工作期只写入 `.artifacts/i18n/quality/runs/`，不进入版本控制。不可重建证据可在
  项目外建立只读归档并记录 manifest/hash，但归档本体不得提交到源码仓库。
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
- Facts packet 的 supplemental-only 语义基线来自 `facts-study-v2`：每项只允许 0–4 条
  真正新增的信息，禁止复述公共 source/context；v1 失败 pilot 保留并自动进入历史
  排除集。最终外部研究使用 curation 协议 `facts-study-v5`、sample/preregistration v2
  和 Fact packet v3，不得把这些版本原地折叠为同一 contract。
- `facts-study-curation-*` 数据流由 `facts-study-curation-build` 生成 80 条 target-blind
  候选池，`facts-study-curation-prepare` 冻结 Facts 后生成 target-visible curator
  bundle，`facts-study-curation-select` 再选择最终 20 条。v3 初始配额为 8
  fact-dependent / 6 surface / 6 clean/acceptable；最终 v5 配额经版本化修订为
  12 / 2 / 6，claim 级门槛仍为 ≥8 addressed、≥8 unaddressed、≥5 clean、≥3 traps。
  natural 优先；controlled 只允许补 fact-dependent 缺口且永不授予 clearance。
- v2 preregistration 默认固定为 `status=offline-frozen`，只有另建并严格绑定用户授权的
  execution manifest 后才允许外部执行。已完成的 33-slot campaign 不产生任何后续
  授权：正式决策为 `do-not-promote-facts-channel`，`holdout_clearance=false`。
  `facts-study-bundles/validate/report` 继续按 artifact contract 自动分派；fake replay
  固定标记为 `non-evidentiary-offline-replay`，natural/controlled 指标分离。Facts
  statement 统一使用英文元语言。
- 共享 claim/contract 核心位于 `tools/i18nlib/quality_contracts.py` 与
  `tools/i18nlib/quality_claims.py`；v2/v3/Facts 旧模块保留原导出名，通过 re-export
  调用公共实现，历史 contract/artifact 不变。

## v3 校准 campaign 状态（2026-08-16）

`stability-preregistration-v2.json` 及其冻结输入为
**`inactive / deferred due to route incompatibility`**。文件字节不改动，
contract 身份、`preregistration_id` 和全部冻结 hash 原样保留，不退役、
不重解释。

延期范围：v3 calibration 的 8 个传输槽、holdout clearance、正式 120 条、
M5 人工裁决、M6 报告、Gold/Silver TM 投产。

理由（按依赖顺序）：

1. **路由不兼容**：prereg v2 冻结的 `prompt_sha256` 与四个 `bundle_sha256`
   由已退役的 blind runner 生成；现行 Paseo `translation_contextual_v1`
   使用完全不同的 envelope、短 prompt 与 `candidate_identity` 结构，
   无法满足这些冻结输入。若启动，必须新建 preregistration 版本。
2. **无映射契约**：语境结果（三键、`additionalProperties=false`）到 v3
   assessment/finding/match/stability 尚无 fail-closed 映射，
   `context_sufficient` 等字段无来源（见 `docs/translation-quality-phase-1.md`
   §4.4 与 §7.2）。
3. **第二 evaluator 未定**：语境契约的运行元组固定为
   `pi/opencode-go/deepseek-v4-flash`，不允许回退 Codex；prereg v2 的
   `reviewer-b`（`gpt-5.6-luna`）在现行路由下无法成立，且未取得译文 bundle
   外发授权。
4. **价值派生于未启动的下游**：8 槽测的是各 evaluator 的重复稳定性，其决策
   意义在于该 evaluator 能否充当正式 120 条中的一份完整 assessment。该链条
   每一环均处于 defer，校准结果当前无可兑现的下游。
5. **无标注对照**：`quality-audit-003` 的 20 条全 `OK` 为单模型、无已知
   正负标签的实战 smoke，不能作为召回、稳定性或一致性证据。

解除条件：明确准备启动正式评价链时，须同时完成 —— 新 preregistration
版本、语境结果到 v3 artifact 的 fail-closed 映射契约、第二独立 evaluator 的
provider/model 选定与外发授权、人工先标注的分层对照集。四项缺一不启动。

口径备注：`host_technical_derivation_agreement` 由宿主用同一函数从同一
sample 的 `gate_signals` 重新派生（`tools/i18nlib/quality_v3.py`
`_host_gate_derivation`），与模型输出无关，同版本代码下结构上恒为 `1.0`。
它是实现回归断言，不是需要实验估计的模型指标；新建 preregistration 时应
重新分类为“provider 调用前的宿主不变量”。此重分类**不减少** 8 槽预算 ——
8 槽来自“两 evaluator × 两轮 × 两 shard”，与该指标无关。

## 身份约定

质量条目的身份轴为 Pilot A `tu_uid`/`revision_uid`（跨文件移动/source-tag 拼写
变化稳定），并保留 editorial `unit_id` 作为证据字段：

- `unit_id`：复用 `stable_entry_id`（component/section/source/source_tag 的
  SHA-256 editorial key），仅作 editorial 证据，不参与修订身份。
- `tu_uid`：Pilot A 单位身份。优先从 identity index（
  `.artifacts/i18n/identity/current/<component>/`）的 editorial→TU 映射解析；
  一对多 editorial 按 TU 拆分（每 TU 一条目）；无映射时回退到
  `tu/fallback-editorial` scheme（与 `build_finding_records::_bind` 一致）。
- `revision_uid`：Pilot A 源文修订，`sha256("rev\0" + tu_uid + "\0" + source_sha256)`。
- `revision_id`：对 `{identity_contract, version, tu_uid, revision_uid,
  target, args_order, special}` 的规范 JSON（UTF-8、键排序、无多余空白）取
  SHA-256；行号和 ordinal 不参与身份。source 或 target/`args_order`/`special`/
  版本变化时 `revision_id` 必变；文件移动或 source-tag 拼写变化（strong TU
  稳定）时 `revision_id` 不变。
