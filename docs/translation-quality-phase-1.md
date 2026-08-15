# 翻译质量系统第一阶段：质量清单与校准试点

> 状态：实施计划 v0.1。M0–M3 已实现并通过门禁（2026-08-04）：
> `i18n/quality/taxonomy-v1.json`、`policy-v1.json`、四份 schema、
> `tools/i18nlib/quality.py` 与 `tools/i18n quality {inventory,sample,validate,report}`；
> 全量 inventory 30,177 个 revision（确定性 SHA-256 已验证），
> 120 条试点样本满足全部覆盖约束且可逐字节复现。
> M4 dry-run 已完成（2026-08-04）：12 条 dry-run 样本由 reviewer-a/reviewer-b 完成
> 两份完整 assessment 并经裁决（strict validate 通过，κ=0.92），报告管线在 dry-run
> 集上全链路验证；`quality validate` 新增 `--dry-run` 模式（adjudication 可选）。
> AI evaluator 隔离 runner 已完成首轮双模型盲测：`deepseek/deepseek-v4-flash` 与
> `openai-codex/gpt-5.6-luna` 均以 max thinking 完整覆盖 12 条并通过 strict validation；
> 最佳校准轮实质缺陷一致率 83.33%、major-or-worse 91.67%，但 severity κ=0.5833，
> 尚未达到 0.70 目标，因此正式 120 条两轮评价与 M5/M6 暂未启动。
> 上位设计：[`translation-quality-system.md`](./translation-quality-system.md)。
> 下一版 evaluator 落地方案：
> [`translation-quality-evaluator-v2.md`](./translation-quality-evaluator-v2.md)。
> 本阶段性质：建立可验证的数据契约和小规模校准基准，不建设生产级模糊匹配。

## 一、阶段目标

第一阶段要回答的不是“30,000 余条译文各是多少分”，而是先验证以下基础是否可靠：

1. 能否稳定识别同一 editorial unit 的不同译文 revision；
2. 能否把现有 lint、术语、运行时键和版本信息转成逐 revision 的确定性门禁；
3. MQM 错误代码、严重程度和文本 profile 是否足够明确，使不同评审者得到可接受的一致性；
4. 能否生成一组可复现、覆盖主要文本类型和风险模式的校准样本；
5. 能否在不改规范 Lua、不隐式联网的前提下完成评价、裁决和报告；
6. 哪些自动信号有资格参与后续 Candidate/Silver/Gold 分层，哪些只能用于风险排序。

本阶段结束时应得到：

- 一份完整但不作语义认证的 current revision inventory；
- 一套机器可校验的 v1 taxonomy、policy 和数据 schema；
- 一份 120 条、双重独立评价并完成裁决的试点基准；
- 一份评价一致性、错误分布、上下文充分性和下一阶段 Go/No-Go 报告。

## 二、明确不做的事项

- 不根据现有全量 Pi “无 finding”结果批量晋级 Gold；
- 不把历史 finding 数量直接换算成当前译文分数；
- 不实现 embedding、向量数据库、模糊搜索 UI 或自动联想；
- 不从整句自动抽取可复用短语；
- 不自动写入或重排规范 Lua、`terminology/` 或发布 addon；
- 不在 quality 命令中自动调用外部 provider；
- 不在试点完成前确定统一加权总分和 Gold 的大规模晋级阈值。

## 三、预期交付物

### 3.1 版本控制中的规则和实现

建议在实际实施时增加：

```text
i18n/quality/
  README.md
  taxonomy-v1.json
  policy-v1.json
  schemas/
    inventory-v1.schema.json
    assessment-v1.schema.json
    adjudication-v1.schema.json
    benchmark-v1.schema.json

tools/i18nlib/quality.py
tests/i18n/test_toolchain.py        # 增加质量系统测试
```

试点裁决通过验收并获得明确批准后，再增加：

```text
i18n/quality/benchmarks/pilot-v1.jsonl
```

规则文件和 schema 是权威配置；全量 inventory、抽样中间文件、评审原始输出和报告不是权威源，不进入版本控制。

### 3.2 `.artifacts` 中的派生文件

建议统一写入：

```text
.artifacts/i18n/quality/runs/<timestamp>-inventory/
  inventory.jsonl
  inventory-summary.json
  inventory-manifest.json

.artifacts/i18n/quality/runs/<timestamp>-sample/
  sample.json
  assessment-template-a.json
  assessment-template-b.json
  sample-manifest.json

.artifacts/i18n/quality/runs/<timestamp>-validation/
  validation.json
  normalized-assessments.jsonl
  normalized-adjudications.jsonl

.artifacts/i18n/quality/runs/<timestamp>-report/
  report.json
  report.md
```

所有 artifact 路径只能使用仓库相对逻辑路径或 artifact 内部相对路径；JSON 内容不得写入主机绝对路径。

### 3.3 建议 CLI

保持 `tools/i18n` 为统一入口，建议增加一个带子动作的 `quality` 命令：

```bash
# 生成 current revision 清单
python3 -B tools/i18n quality inventory --json

# 从清单确定性抽取试点样本
python3 -B tools/i18n quality sample \
  --inventory <inventory.jsonl> \
  --size 120 \
  --seed tome4-quality-pilot-v1 \
  --json

# 严格校验两份评价和裁决
python3 -B tools/i18n quality validate \
  --sample <sample.json> \
  --assessment <reviewer-a.json> \
  --assessment <reviewer-b.json> \
  --adjudication <adjudication.json> \
  --strict \
  --json

# 生成聚合报告
python3 -B tools/i18n quality report \
  --validation <validation.json> \
  --json
```

如果第一版 CLI 不采用 argparse 嵌套 subparser，可以临时使用等价的单层参数，但 artifact contract 和命令语义不得因此改变。

## 四、数据契约

### 4.1 身份轴：Pilot A `tu_uid`/`revision_uid` 桥接 + 译文修订

质量条目的单位身份使用 Pilot A TU 身份（infra-contract-007 迁移）：

```text
tu_uid = identity index editorial→TU 解析（无映射回退 tu/fallback-editorial）
revision_uid = SHA256("rev\0" + tu_uid + "\0" + source_sha256)
```

在此基础上新增译文修订：

```text
revision_id = SHA256(
  identity_contract,
  game_version,
  tu_uid,
  revision_uid,
  target,
  args_order,
  special
)
```

`unit_id`（editorial `stable_entry_id`）保留为证据字段，不再参与修订身份。
具体实现使用 UTF-8、键排序、无多余空白的规范 JSON。必须满足：

- source 或 target、`args_order`、`special`、游戏版本变化时，`revision_id` 必变；
- 仅行号、ordinal 或文件重排变化时，`revision_id` 不变；
- 文件移动（section 变）或 source-tag 拼写变化而 strong TU 稳定时，
  `tu_uid`/`revision_uid`/`revision_id` 均不变（谱系存活）；
- 一对多 editorial（同一 editorial key 对应多个 strong TU）按 TU 拆分为多条，
  每条携带自己的 `tu_uid`/`revision_uid`/`revision_id`；
- 相同 editorial key 的合法重复 occurrence 在所属 TU 条目内单独记录 occurrence；
- 不允许用 target 归一化结果计算身份。

### 4.2 inventory envelope

`inventory-manifest.json` 至少包含：

```json
{
  "schema_version": 1,
  "quality_contract": "tome4-quality-inventory-v1",
  "tool_version": "...",
  "version": "tome-1.7.6",
  "manifest_sha256": "...",
  "translation_inputs_sha256": "...",
  "terminology_sha256": "...",
  "inventory_sha256": "...",
  "entries": 0,
  "components": {},
  "profile_classifier_version": "profile-v1",
  "risk_rule_version": "risk-v1"
}
```

时间戳和本地输出路径不参与 `inventory_sha256`，保证相同输入产生相同内容身份。
`translation_inputs_sha256` 按 manifest 顺序覆盖每个 component 的
`copy_fragment`（若有）和 `translation`：摘要材料逐项记录 component、role、
逻辑路径及原始字节 SHA-256，同一路径的多次消费不得去重。

### 4.3 inventory 条目

每条 `inventory.jsonl` 至少包含：

| 字段 | 要求 |
|---|---|
| `unit_id` / `revision_id` | 64 位小写 SHA-256；`revision_id` 用 Pilot A 桥接公式 |
| `tu_uid` / `revision_uid` | 64 位小写 SHA-256（Pilot A 单位身份 / 源文修订） |
| `version` / `component` | 与 manifest 一致 |
| `section` / `source` / `target` | 原始规范字符串，不做身份归一化 |
| `source_tag` | 字符串或 `null` |
| `args_order` / `special` | 保留 Lua loader 的规范值 |
| `occurrences` | 仅含相对逻辑路径、section、line 等位置元数据 |
| `profile` | v1 白名单值 |
| `profile_confidence` | `high / medium / low` |
| `domain_hints` | 从相关术语和 section 推断的有界列表 |
| `relevant_terms` | 相关术语的稳定引用、status 和适用性，不复制无关术语表 |
| `structure` | printf、markup、token、换行等签名 |
| `gate_signals` | 事实信号，不提前伪造人工 pass |
| `risk_flags` | v1 白名单标志 |
| `source_length_bin` | 固定长度桶 |

`line` 只能用于定位，不能参与质量结论身份。不得写入源码仓库或 DLC 目录的绝对路径。

### 4.4 assessment

每位评审者对每个 revision 提交一条 assessment：

```json
{
  "schema_version": 1,
  "quality_contract": "tome4-quality-assessment-v1",
  "sample_id": "...",
  "evaluator": {
    "kind": "human",
    "id": "reviewer-a",
    "method_version": "mqm-pilot-v1"
  },
  "items": [
    {
      "revision_id": "...",
      "context_sufficient": true,
      "profile_confirmed": "mechanics",
      "findings": [
        {
          "finding_id": "A-001",
          "error_code": "ACC_CONDITION",
          "severity": "major",
          "source_span": "...",
          "target_span": "...",
          "body": "...",
          "evidence_refs": []
        }
      ],
      "reuse_recommendation": "same-tag"
    }
  ]
}
```

约束：

- assessment 必须覆盖 sample 中全部 revision，除非 contract 明确允许 partial；试点默认不允许 partial；
- `finding_id` 仅在该 assessment 内唯一，规范 identity 由宿主生成；
- 错误代码、severity、profile、reuse scope 必须来自 policy 白名单；
- `note` 只能表示可选建议，不得与“存在实质缺陷”混用；
- 上下文不足时必须设置 `context_sufficient=false`，不能猜测机制并强行给出 clean 结论；
- 证据引用只允许指向 sample 内术语、相对公开源码证据记录或受审计 artifact ID；
- evaluator ID 使用稳定代号，不写个人敏感信息。

如果 evaluator 是模型，还必须记录 provider、model、thinking、prompt SHA-256 和 bundle ID；同一缓存输出不得伪装成第二位独立评审者。

### 4.5 adjudication

裁决记录必须逐 revision 绑定两份 assessment：

```json
{
  "schema_version": 1,
  "quality_contract": "tome4-quality-adjudication-v1",
  "sample_id": "...",
  "items": [
    {
      "revision_id": "...",
      "assessment_ids": ["...", "..."],
      "context_sufficient": true,
      "resolved_findings": [],
      "quality_vector": {
        "accuracy": 4,
        "mechanics_context": 4,
        "terminology": 4,
        "fluency": 3,
        "style": null,
        "ui_render": null,
        "corpus_consistency": 4
      },
      "confidence": "C3",
      "provisional_grade": "Gold",
      "reuse_scope": "same-tag",
      "rationale": "..."
    }
  ]
}
```

试点中的 grade 必须标记为 `provisional`。只有本阶段整体通过并经明确批准后，才能把裁决样本作为正式 benchmark 或后续 TM 种子。

## 五、确定性 inventory 实现

### 5.1 输入

只读取：

- 选定 manifest；
- manifest 声明的规范翻译 Lua；
- `terminology/`；
- `i18n/policy.json`；
- 质量 taxonomy/policy；
- 本地确定性扫描结果应由当前运行重新计算，不依赖“最新目录”猜测。

copy fragment 继续由现有 lint/build 流程校验，但其中不属于 `t(...)` 的运行配置不进入整句质量 inventory。

历史 review/remediation 可以在后续作为显式 `--evidence-index` 输入。第一版若不能严格验证其 revision 绑定，应完全不导入，而不是用 source 或行号近似关联。

### 5.2 复用现有实现

- 使用 `LocaleLoader`，不得另写正则解析 Lua；
- 使用 `stable_entry_id`、`extract_format_tokens`、`MARKUP_RE` 和 `AT_TOKEN_RE`；
- 运行时键语义复用 lint/collision 工具，不建立相冲突定义；
- 术语匹配复用 workset 的 scope/source_tag 边界逻辑，但应记录精确匹配依据；
- report/run directory 复用 `create_run_directory` 和原子 JSON 写入工具。

### 5.3 profile v1 分类优先级

建议按以下优先级推断，命中冲突时降低置信度而非静默覆盖：

1. 明确 `source_tag`：talent、log、chat/say、achievement/lore、UI 等；
2. 相关术语 category：`T.GAME.TALENT`、`T.DIALOGUE.CHAT`、`T.RUNTIME.LOG` 等；
3. section 路径模式：`data/talents`、`data/chats`、`data/lore`、`dialogs` 等；
4. 文本结构：短标签、长叙事、printf 模板；
5. 无充分证据时为 `unknown`。

自动分类只描述文本功能，不评价译文好坏。`profile_confidence != high` 应成为抽样风险信号。

### 5.4 risk flag v1

第一版至少生成以下确定性标志：

```text
has-printf
has-args-order
has-markup
has-at-token
multiline
short-ambiguous-source
long-source
profile-uncertain
preferred-term-present
term-variant-or-review
repeated-runtime-key
source-has-number-or-unit
source-has-negation-or-condition
source-target-length-outlier
possible-untranslated-residue
```

说明：

- risk flag 只用于抽样和审核优先级，不直接扣质量分；
- 长度比、英文残留和否定词检测只能作为提示，必须保守并支持例外；
- `repeated-runtime-key` 不等于冲突，现有大量同 target 合法重复不能被误报为缺陷；
- 历史 confirmed/rejected finding 只有在通过严格 revision 关联后才能增加对应 flag。

### 5.5 自动 gate signal

inventory 只记录可证明的事实，例如：

```text
lua_load_valid=true
empty_target=false
format_signature_match=true
markup_multiset_match=true
at_token_multiset_match=true
runtime_collision=false
```

`semantic_accuracy=true`、`terminology_correct=true`、`context_sufficient=true` 等不能由 inventory 自动生成。自动检查不足时使用 `needs-review`，不得默认 pass。

## 六、120 条试点样本

### 6.1 样本结构

样本分为三个互斥来源桶，报告时分别统计：

| 桶 | 数量 | 用途 |
|---|---:|---|
| `representative` | 60 | 按组件组、profile 和长度分层的代表性随机样本 |
| `risk-enriched` | 40 | printf、markup、术语、条件、长文本、上下文不确定等高风险样本 |
| `contrast` | 20 | 同源不同语境、近似原文、重复运行键或历史争议的对照样本 |

只有 `representative` 桶可以用于非常粗略的总体缺陷率估计；风险桶和对照桶只用于验证 taxonomy 和检测能力。

### 6.2 覆盖约束

在语料存在足够候选的前提下，样本生成器应满足：

- `mechanics`、`term-name`、`ui`、`runtime-log`、`dialogue`、`narrative` 各不少于 8 条；
- `technical-internal` 和 `unknown` 合计不少于 8 条，用于验证边界；
- core、DLC、辅助 addon/示例三个组件组各不少于 20 条；
- 四个 source 长度桶各不少于 15 条；
- 至少 30 条具有 printf/markup/token/多行中的一种结构风险；
- 至少 20 条包含 preferred 或 review/variant 术语证据；
- contrast 桶中的成对条目必须整体入样，不能只抽一侧；
- 同一 `revision_id` 不重复计数。

某约束因语料不足无法满足时，命令必须在 manifest 中显式报告，不得悄悄放宽。

### 6.3 可复现抽样

抽样算法必须：

1. 先按稳定键排序；
2. 使用固定 seed `tome4-quality-pilot-v1`；
3. 将 taxonomy、policy、manifest、规范 Lua 输入、术语表、inventory SHA-256、
   inventory 生成工具版本和 seed 纳入 `sample_id`；
4. 在相同输入上生成逐字节相同的 sample 内容；
5. 排除时间戳和 artifact 路径对 `sample_id` 的影响。

如规则变化，提升 sample contract 或 seed 名称，不覆盖历史样本身份。
official 与 dry-run sample identity 均携带 `translation_inputs_sha256`、
`terminology_sha256` 和 `inventory_tool_version`；验证和报告必须针对当前输入重新
核验这些绑定，而不是重建 inventory 或重新加载 Lua。

## 七、评审与裁决协议

### 7.1 评审输入

每条 sample item 提供一个有界 context packet：

- source、target、component、section、`source_tag`；
- `args_order`、`special` 和结构签名；
- 自动推断 profile 及其置信度；
- 相关术语行及 notes；
- 同组 contrast 条目；
- 必要时最多前后各两条规范译文作为局部上下文；
- 明确的“不足上下文”选项。

第一轮独立评审默认不展示历史 finding、另一评审者结论或预期 grade，降低锚定效应。自动技术事实可以展示，但不得把启发式风险标志写成既定错误。

### 7.2 两次独立评价

每个 revision 由两位 evaluator 独立完成：

- 两位 evaluator 都必须具备理解 source 和判断中文 target 的能力，其中至少一位熟悉对应游戏文本类型；
- mechanics 争议需要由主代理或人工在固定版本源码行为上核验；
- 第一轮试点默认以人工结构化 assessment 为准；现有 Pi finding-only 审核可作为辅助问题发现信号，但因不逐条声明 clean 结论，默认不替代其中一次完整 assessment；
- 如以后让 Pi 承担完整 evaluator，必须先在现有 `tools/i18n review` / `tools/pi-tmux review` 入口内设计并测试有界质量模式，继续使用 `$tome4-pi-review`，并履行 provider、model、bundle 类型和条目数量授权；不得另建绕过现有协议的直连入口；
- 未经授权时，质量命令最多生成本地 bundle/template，不启动 provider；
- 同一模型、提示和缓存结果不算两次独立评价。

### 7.3 裁决顺序

1. 比较两份 assessment 的 context sufficiency、是否有实质缺陷和 major-or-worse 判定；
2. 对错误跨度、代码和 severity 做匹配；
3. 对不一致项读取双方理由，不先采用多数表决；
4. 机制争议按固定源码实际行为裁决，并记录 commit 与关键调用/定义；
5. 原文自身错误使用 `SOURCE_*`，明确译文是否为有意修正；
6. 产出 resolved findings、质量向量、confidence、provisional grade 和 reuse scope；
7. 裁决者不得在同一步直接修改规范 Lua。发现真实问题时另建后续 remediation 工作项。

### 7.4 finding 匹配

用于一致性统计时，两个 finding 满足以下条件可视为同一问题：

- `revision_id` 相同；
- 一级类别相同；
- 错误代码相同，或经 policy 声明为可合并近邻代码；
- target/source span 相交，或双方明确引用相同参数/术语；
- severity 差异单独统计，不阻止问题身份匹配。

不得仅凭标题文本相似度合并 finding。

## 八、报告和校准指标

### 8.1 必须报告

`report.json` 和 `report.md` 至少包含：

- inventory 总数、按 component/profile/长度/risk 的分布；
- 样本约束满足情况和每个来源桶的构成；
- 两位 evaluator 的覆盖完整性；
- context sufficient 一致率；
- “是否存在实质缺陷”的一致率；
- “是否存在 major/blocker”的一致率；
- error category precision/recall/F1（互相作为比较对象，不冒充真值）；
- severity 加权一致性；
- 经 adjudication 后的错误类型和严重程度分布；
- `SOURCE_*`、`CTX_INSUFFICIENT`、未知/无法归类问题比例；
- provisional grade/confidence/reuse scope 分布；
- 自动 risk flag 对 confirmed finding 的命中情况；
- 需要修改 taxonomy、profile 或 context packet 的具体清单。

### 8.2 校准目标

以下是进入 400 条正式基准扩展前的目标，不是通过粉饰数据强行达到的发布门槛：

- assessment schema 有效和样本覆盖率：100%；
- major-or-worse 有无的一致率：目标不低于 90%；
- 任意实质缺陷有无的一致率：目标不低于 80%；
- severity 加权一致性：目标 `κ >= 0.70`；
- 无法映射到 taxonomy 的 confirmed 问题：低于 5%；
- 因 context packet 不足而无法裁决：低于 10%；
- 所有 provisional Gold 均通过适用的确定性门禁，且无 unresolved confirmed finding。

若未达到目标，应修改 rubric/context/taxonomy，并对固定 overlap 子集重新盲评；不得通过删除争议样本提高一致率。

### 8.3 禁止误读

- 60 条 representative 仍只是试点，不能生成精确的全语料质量声明；
- 40 条 risk-enriched 的缺陷率不能外推到全语料；
- evaluator 一致不代表双方一定正确，仍需 adjudication；
- 自动风险规则高召回不等于适合做硬门禁；
- provisional Gold 只用于验证规则，不自动进入生产 TM。

## 九、实施任务顺序

### M0：冻结文档决策

- 审阅并确认本方案的三轴模型、taxonomy、severity、profile 和试点规模；
- 确认哪些数据允许进入版本控制，哪些只能留在 `.artifacts`；
- 确认第一轮 evaluator 组成；如涉及外部 provider，另行完成授权。

**完成条件：** 文档中的未决项有明确裁决，实施不需要临时发明新等级。

### M1：建立 schema 与 policy

- 新增 `i18n/quality/` 规则文件；
- 为 taxonomy、profile、severity、reuse scope 建立白名单；
- 定义规范 JSON hashing 和严格 unknown-field 行为；
- 增加 schema 及 identity 单元测试。

**完成条件：** 合法 fixture 通过；未知代码、绝对路径、错误 hash、stale revision 和重复 assessment 被拒绝。

### M2：实现 inventory

- 通过 `LocaleLoader` 加载 manifest 声明的全部规范译文；
- 聚合 occurrence，生成 unit/revision、结构签名、profile 和风险事实；
- 复用 lint/术语/运行时键逻辑；
- 写入 content-addressed artifact 和摘要报告。

**完成条件：** inventory 条目/occurrence 数与 loader 结果守恒；相同输入重复运行的内容 SHA-256 相同。

### M3：实现确定性抽样

- 实现三个来源桶、覆盖约束、成对 contrast 和固定 seed；
- 生成 assessment templates；
- 对样本 contract 和路径边界做严格验证。

**完成条件：** 重复运行逐字节一致；120 个唯一 revision；所有可满足约束均满足，例外显式报告。

### M4：完成两轮独立评价

- [x] 12 条 dry-run 条目：reviewer-a/reviewer-b 两份完整 assessment + 裁决已完成并冻结
  （`.artifacts/i18n/quality/runs/*-dry-run/dry-run-frozen-manifest.json`，strict validate
  通过，报告管线全链路验证）；rubric 观察 OBS-001–004 已记录（profile 分类：物品未识别名/
  天赋名应归 term-name、zones 长叙事应归 narrative、术语表缺组合实体词、contrast 身份记账）。
- [x] `quality validate` 支持 `--dry-run`（dry-run contract 样本 + adjudication 可选）。
- [x] 新增 `tools/pi-quality-evaluator` 与 `i18n/prompts/pi-quality-evaluator.md`：模型无工具、
  无会话、无项目上下文，bundle 不含另一 assessment、裁决、历史 finding 或预期 grade；宿主固定
  evaluator 身份并严格校验 100% revision 覆盖，精确缓存按 provider/model/thinking/prompt/bundle 隔离。
- [x] 两个真正独立模型完成多轮 12 条盲测（DeepSeek V4 Flash 与 GPT-5.6 Luna，均 max）：首轮
  4/14 findings、缺陷一致率 50%、κ=0.1875；统一逐项检查表后的最佳轮为 9/13 findings、缺陷一致率
  83.33%、major-or-worse 91.67%、κ=0.5833。第三轮 severity 锚点复测因模型随机差异回落至
  7/14 findings、缺陷一致率 58.33%、κ=0.34；另捕获并回归测试了一次“完整 items 数组仅缺最外层
  右花括号”的模型输出，宿主只允许该唯一确定性 envelope 修复，其他畸形输出继续拒绝。
- [ ] 当前 AI evaluator 对“是否有缺陷”已曾达到目标，但 severity 稳定性仍未达到 κ≥0.70；不得
  为提高指标删除争议样本或挑选单次结果。需先冻结 AI rubric/prompt 版本，并在新的固定 overlap
  子集复测或决定由人工承担 severity 裁决，之后两位 evaluator 才从头完成正式 120 条；每份
  assessment 严格校验后冻结 content hash。

**完成条件：** 两份 assessment 均覆盖正式 120 条、schema 有效、相互独立且绑定 sample ID；dry-run 不计入正式一致性和缺陷率。

### M5：人工裁决

- 生成 disagreement workset；
- 对语义、severity、上下文和 reuse scope 逐项裁决；
- 必要时核验固定源码机制；
- 真实译文问题进入独立 remediation 队列，本阶段不就地修 Lua。

**完成条件：** 120 条均有唯一 adjudication；没有未知 finding、悬空 assessment 或未说明上下文缺口。

### M6：报告与 Go/No-Go

- 生成机器和人类可读报告；
- 对照校准目标；
- 决定保持 taxonomy v1、修订后重试，或停止扩展；
- 明确批准后才把去除运行路径和未裁决内容的 immutable pilot benchmark 写入版本控制。

**完成条件：** 报告可由 sample + assessments + adjudication 确定性重建，且明确记录下一阶段决策。

## 十、测试计划

### 10.1 身份和失效测试

- target 改一字，revision ID 改变；
- `args_order`、`special`、version 改变，revision ID 改变；
- source 变化（revision_uid 变）或 source-tag 拼写变化导致 editorial 改映射时，revision ID 改变；
- 只改 line/ordinal，revision ID 不变；
- 文件移动（section 变）或 source-tag 拼写变化而 strong TU 稳定时，`tu_uid`/
  `revision_uid`/`revision_id` 均不变（谱系存活）；
- 旧 assessment 不能绑定新 revision。

### 10.2 结构和分类测试

- `%%` 不被当作参数；
- 参数 permutation 与 `args_order` 一致；
- markup/token 使用多重集合而非普通集合；
- profile 冲突降置信度或进入 `unknown`；
- 合法重复运行键不被标记为 collision；
- 数字、否定词和长度异常只生成 risk flag，不生成 MQM 缺陷。

### 10.3 抽样测试

- 相同 seed 和 inventory 产生相同 sample ID/内容；
- 不同 seed 改变选择但仍满足覆盖约束；
- contrast pair 不被拆分；
- revision 不重复；
- 不可能约束产生结构化 warning，而非静默失败；
- representative/risk/contrast 桶互斥且总数精确为 120。

### 10.4 assessment/adjudication 安全测试

- 拒绝未知 error code、severity、profile、reuse scope；
- 拒绝未知 revision、重复 finding ID 和不完整覆盖；
- 拒绝绝对路径及 `..` 路径；
- 拒绝 assessment/sample ID 不匹配；
- 拒绝 adjudication 引用不存在的 assessment；
- 拒绝存在 confirmed blocker/major 时晋级 Gold；
- rejected observation 不错误降低当前 quality vector。

### 10.5 集成和回归测试

实施代码完成后至少运行：

```bash
python3 -B tools/i18n doctor
python3 -B tools/i18n lint --strict
python3 -m unittest -q tests/i18n/test_toolchain.py
python3 -B tools/scan_runtime_collisions.py
python3 -B tools/classify_runtime_keys.py
git diff --check
```

若实施过程中修改术语表或批量译文，还必须按 `AGENTS.md` 运行对应的完整术语审计和门禁；本阶段原则上不应修改这两类规范内容。

## 十一、阶段验收标准

只有同时满足以下条件，阶段 1 才算完成：

- [ ] v1 taxonomy、policy 和 schema 已版本化并有测试；
- [ ] 全量 inventory 能由当前 manifest/规范 Lua 确定性重建；
- [ ] inventory 与 `LocaleLoader` 条目和 occurrence 数守恒；
- [ ] artifact 不含主机绝对路径，不改规范 Lua；
- [ ] 120 条 sample 唯一、可复现并满足或显式说明覆盖约束；
- [ ] 两份独立 assessment 完整且通过 strict validation；
- [ ] 120 条均完成 adjudication，并绑定当前 revision；
- [ ] report 区分 representative、risk-enriched 和 contrast；
- [ ] 所有 provisional Gold 通过门禁且无 unresolved confirmed finding；
- [ ] 评价一致性和 taxonomy 缺口已有明确结论；
- [ ] 全部项目门禁通过，工作树无意外生成物；
- [ ] 是否扩展到 400 条正式 benchmark、是否开始 Gold/Silver 精确 TM 已由用户明确决定。

## 十二、失败处理与回滚

- inventory/sample 失败：删除对应 `.artifacts/i18n/quality/runs/` 即可，不触碰规范数据；
- schema/taxonomy 设计错误：在 benchmark 晋级前修订 v1 草案；已有外部使用后必须升级 contract，不原地改变语义；
- 评审一致性不足：冻结原始 assessment，修订 rubric 后对固定 overlap 子集重新盲评；
- 发现大量真实译文问题：生成独立 remediation 队列，按现有流程分批处理和复审，不在质量标注文件中直接改 target；
- 外部 provider 未授权或失败：保留 bundle/template，改用人工评审或等待授权，不降低隔离要求；
- 任一脚本产生规范 Lua、术语表或外部仓库改动：立即停止，以 Git diff 核查并撤销非预期写入。

## 十三、阶段结束后的决策

阶段报告应明确给出以下决策之一：

1. **Go：扩展基准。** taxonomy 和协议稳定，将样本扩展到约 400 条；
2. **Go with changes：修订后扩展。** 保留原始试点，升级 rubric/policy 并复评 overlap 子集；
3. **Exact-only：只建精确库。** 证据足以筛选 Gold/Silver，但上下文分类不足以支持模糊匹配；
4. **No-Go：返回基础数据治理。** revision 关联、上下文或评审一致性尚不足，暂不建立译文库。

任何一种决策都必须基于 report 中的证据，而不是为了推进功能而默认选择 Go。
