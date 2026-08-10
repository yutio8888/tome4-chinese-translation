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
| `reviewer-comparison-v1.json`、`reviewer-comparison-v2.json` / `schemas/reviewer-comparison-*.schema.json` | `tome4-reviewer-comparison-*` | 生产 translation semantic v2 审核模型的 32+32 盲测；v2 分离语义差异与人工可接受性、声明 Gold 穷尽性并使用语义 claim 稳定性 |
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

## 生产 v2 审核模型对比

`reviewer-comparison-v2.json` 固定 DeepSeek v4 Flash `max` 与 GPT-5.6-sol
`medium` 的 32+32 盲测。v1 首轮校准因模型结构失败、claim 不稳定以及 Gold
把“人工可接受”误作“无可观察语义差异”而被拒绝；v2 是破坏性契约升级，旧
freeze 不得续跑或按新指标重解释。该流程只生成和校验本地 artifact，不会自动
调用 provider：

```bash
python3 -B tools/i18n quality reviewer-compare-prepare --inventory <inventory.jsonl>
python3 -B tools/i18n quality reviewer-compare-freeze --pool <candidate-pool.json> --gold <human-gold.json>
python3 -B tools/i18n quality reviewer-compare-validate --preregistration <preregistration.json> --result-index <result-index.json>
python3 -B tools/i18n quality reviewer-compare-report --validation <validation.json>
```

- `prepare` 排除 dataset registry 的所有历史 revision，优先从 `tome` 与三个官方
  DLC 生成 256 条人工筛选候选。若风险排序池缺少人工已确认所需的自然
  `context-insufficient` 类型，可用重复的 `--include-revision <sha256>` 显式补充当前
  inventory 中尚未注册的自然 revision；补充列表进入 candidate-pool 内容身份，缺失、
  重复、非法或已注册 revision 均失败关闭，不能以此注入受控改写。
- `freeze` 只接受明确 `human_confirmed=true` 的 32+32 Gold。每项分别记录
  `semantic_state`、人工 severity/可接受性和 `findings_exhaustive`：
  `no-substantive-difference` 才可进入误报分母；`substantive-difference + clean`
  表示差异存在但人工可接受（包括经源码确认合理的机制适配）。是否需要源码核验来
  判断“可接受”不等于 bounded 文本 `context-insufficient`；后者只用于缺失指代、附着、
  省略或刻意歧义导致无法判断文本命题的情况。非穷尽 Gold 上额外观察只进入待裁决计数，不自动算
  false positive。每条必检 claim 还须列出人工认可的 `accepted_classifications`。
  `adjudication_rationale` 记录为何属于真实等价、可接受差异或不可接受差异；存在
  多种合法 taxonomy 表达时，finding 的 `classification_rationale` 记录等价理由。
  这些宿主裁决字段不进入 blind provider payload。
  freeze 同时检查最低 major/substantive/clean、至少 12 条真正无实质差异、至少 2 条
  “有差异但可接受”的 clean、至少一条 context-insufficient、组件多样性和
  `fallback_stage`，并生成与生产 translation semantic v2 完全相同的 bundle。
  报告会以 `precision_complete=false` 标记仍有未裁决额外 finding 的 run；这种 run
  不得通过次级 precision/recall 判胜规则。
- 冻结后的 slot 包含显式 `--no-cache`、模型、thinking、bundle identity 和
  1200 秒超时命令；只允许纯传输失败重试一次。真实执行前仍必须按
  `AGENTS.md` 报告准确 payload 并单独取得用户外发授权。
- 受控语义扰动不是 canonical revision，不得混入生产 v2 bundle。
  `controlled-semantic-variants` 回退只能进入单独的辅助实验，不足以产生生产模型切换结论；
  本流程会对尝试将其混入生产 bundle 的输入失败关闭。
- v2 校准 bundle 最多 2 条且总字符预算 16,000。DeepSeek `max` 在一次三条、约
  24,000 item 字符的 bundle 中再次遗漏完整条目，因此后续冻结进一步缩小边界；生产
  translation v2 的 10 条硬上限不
  因此自动改变。模型返回完整、唯一且恰好相同的 revision 集但仅顺序错误时，
  normalizer v4 按 bundle 确定性复序并在 summary 计数；缺失、重复或未知 revision
  继续失败关闭。
- result index 的每个 slot 显式标记 `pending`、`success` 或
  `content-structure-failure`。内容/结构失败必须绑定失败 runner report 与原始输出摘要，
  assessment 必须为空，且 runner report 的 `failure_kind` 必须为
  `content-structure`；成功和失败报告都必须由宿主重算 prompt、policy、normalizer、
  runner 与精确 stdin payload 共同绑定的 cache identity。宿主不会修写非法模型组合，
  也不会用另一请求替换该 slot。
- 校准阶段允许 holdout slot 保持 `pending`。验证器以成功 slot 数计算 schema coverage，
  并按 reviewer 统计 structure failures；两轮稳定性同时报告精确 finding-key Jaccard
  和基于同 revision、重叠 evidence 的 `semantic_claim_jaccard`，准入使用后者及
  finding/no-finding 的 `item_flag_agreement`，不再使用几乎恒为 `assessed` 的 state
  agreement。只有两位 reviewer 同时满足结构、语义稳定性、context state 和真正
  no-difference false-positive 门槛，才产生 `calibration_clearance=cleared`。否则
  clearance 为 `denied`，任何已填入的 holdout 结果或 `holdout_cleared=true` 都会失败
  关闭。holdout 指标只在该 clearance 后计算。

## 身份约定

- `unit_id`：复用 `stable_entry_id`（component/section/source/source_tag 的
  SHA-256 editorial key）。
- `revision_id`：对 `{identity_contract, version, unit_id, target,
  args_order, special}` 的规范 JSON（UTF-8、键排序、无多余空白）取 SHA-256；
  行号和 ordinal 不参与身份。
