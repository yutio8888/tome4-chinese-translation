# 翻译质量 AI Evaluator v2：事实判定、规则定级与匿名裁决

> 状态：设计方案 v0.1，尚未实现。
>
> 适用阶段：翻译质量系统第一阶段 M4–M6。
>
> 上位设计：[`translation-quality-system.md`](./translation-quality-system.md)。
>
> 现行试点：[`translation-quality-phase-1.md`](./translation-quality-phase-1.md)。
>
> 设计背景：现有 12 条双模型盲测证明两个模型能够完整输出 assessment，也能较好地
> 发现翻译问题；但 finding 拆分方式和 severity 标尺不稳定。本文定义下一版可执行协议，
> 不修改或重新解释已经冻结的 v1 assessment、dry-run 和校准结果。

## 一、决策摘要

现阶段停止在原 12 条样本上继续修改提示词、反复运行并追求某一次
`severity weighted κ >= 0.70`。原 12 条已经被多次观察，只能继续作为探索性回归集，
不能再作为泛化验证证据。

v2 采用以下流水线：

```text
双模型独立发现问题
        │
        ▼
问题证据规范化与问题单元匹配
        │
        ▼
模型分别判断可核验的事实维度
        │
        ▼
宿主按版本化规则派生 severity
        │
        ▼
分歧问题匿名人工裁决事实和规则
        │
        ▼
裁决案例进入锚点与回归集
```

核心职责分离如下：

| 角色 | 负责 | 不负责 |
|---|---|---|
| AI evaluator | 发现问题、指出原文/译文证据、判断影响事实、推荐相近锚点 | 自由选择最终 severity、查看另一模型答案、裁决争议 |
| 宿主工具 | 严格校验、规范化 span、匹配问题、应用确定性规则、生成指标 | 猜测缺失事实、修改模型语义结论、自动修改规范 Lua |
| 人工裁决者 | 确认问题是否存在、双方是否描述同一问题、哪些事实成立、规则是否缺失 | 根据模型身份投票、无规则地凭感觉直接选择 severity |

## 二、为什么需要 v2

当前 12 条盲测暴露出三个互相叠加的问题：

1. `major/minor/note` 的自然语言定义仍存在解释空间；
2. 两个模型不一定以相同粒度拆分 finding，现有一对一匹配可能把拆分差异当成判断差异；
3. 12 条中每条占 8.33 个百分点，单个边界案例会显著改变一致率和 κ。

因此，一次 κ 超过 0.70 不能证明标尺稳定；一次低于 0.70 也不足以证明系统不可用。
应把“发现了什么”“事实后果是什么”“规则如何定级”拆开，并扩大且隔离校准数据。

## 三、目标与非目标

### 3.1 目标

- 把 severity 从模型的自由标签改成可追溯的规则派生结果；
- 为每个 finding 建立稳定、可匹配的问题单元；
- 分开统计条目级缺陷发现、问题级匹配、影响事实和 severity 一致性；
- 用少量人工确认的锚点统一边界，而不是堆积大量提示词示例；
- 让人工只处理真实分歧和规则缺口，并让裁决持续转化为回归数据；
- 保持 evaluator 无工具、无会话、无项目上下文和相互盲评；
- 保持全部输出为 `.artifacts/i18n/quality/` 下的派生 artifact，不自动修改译文。

### 3.2 非目标

- 不要求两个模型发现完全相同的所有风格建议；
- 不把 κ 作为唯一可用性指标；
- 不以模型多数表决替代人工事实裁决；
- 不让模型自行生成最终 Gold/Silver 等级；
- 不使用正式 120 条、封存验证集或历史裁决答案来调提示词；
- 不在 v2 中建设模糊翻译记忆或自动应用修订。

## 四、质量、严重度、风险和优先级分离

v2 继续遵守整体质量系统的三轴模型，并进一步区分：

1. **缺陷类别**：语义、术语、表达、风格、技术等；
2. **单条 severity**：这一个 revision 中此问题造成的后果；
3. **传播风险**：同一错误是否可能重复或被翻译记忆扩散；
4. **审核优先级**：severity、玩家暴露、传播范围和上下文不确定性的组合。

不得因为一个标点问题重复出现 100 次，就把每个实例从 minor 升为 major。
重复和扩散进入 `amplification_scope` 与 `review_priority`；只有错误本身造成全局机制误导、
运行破坏或系统性错误时，才影响单条 severity。

建议继续使用：

```text
review_priority = defect_likelihood × impact × player_exposure × reuse_amplification
```

该值不参与 severity 派生。

## 五、v2 Assessment 数据模型

v2 是破坏性契约变更，不能原地扩展并重新解释
`tome4-quality-assessment-v1`。建议新增：

```text
assessment_contract = tome4-quality-assessment-v2
method_version      = mqm-pilot-v2
```

现有 v1 assessment、adjudication 和 report 保持不可变。

### 5.1 Assessment envelope

宿主继续拥有 evaluator 身份，不允许模型自行填写 provider、model、prompt hash 或 bundle ID：

```json
{
  "schema_version": 2,
  "quality_contract": "tome4-quality-assessment-v2",
  "sample_id": "...",
  "evaluator": {
    "kind": "model",
    "id": "reviewer-a",
    "method_version": "mqm-pilot-v2",
    "provider": "...",
    "model": "...",
    "thinking": "...",
    "prompt_sha256": "...",
    "rules_sha256": "...",
    "anchors_sha256": "...",
    "bundle_ids": ["..."]
  },
  "items": []
}
```

模型只返回 `items`；宿主补齐并校验 envelope。

### 5.2 Item

```json
{
  "revision_id": "...",
  "context_sufficient": true,
  "profile_confirmed": "mechanics",
  "findings": [],
  "reuse_recommendation": "same-tag"
}
```

`context_sufficient=false` 表示不能可靠判断关键事实，不表示该条自动 clean。

### 5.3 Finding

模型 finding 不再包含自由选择的 `severity` 或最终 `rule_id`：

```json
{
  "finding_id": "A-001",
  "error_code": "ACC_NUMBER_UNIT",
  "defect_class": "semantic",
  "phenomenon": "number-range",
  "source_evidence": {
    "quote": "3–8 damage",
    "occurrence": 1
  },
  "target_evidence": {
    "quote": "8点伤害",
    "occurrence": 1
  },
  "defect_summary": "浮动范围被译成固定上限",
  "meaning_change": {
    "type": "strengthened",
    "summary": "技能效果被表达为稳定达到上限"
  },
  "impact_facts": {
    "is_defect": "yes",
    "is_substantive": "yes",
    "mechanics_context": "yes",
    "changes_rule_understanding": "yes",
    "can_change_player_action": "yes",
    "required_operation_info_missing": "no",
    "opposite_or_different_rule": "no",
    "recoverable_from_immediate_context": "no"
  },
  "amplification_scope": "local",
  "closest_anchor_id": "S-NUM-01",
  "anchor_relation": "meets",
  "body": "最低值丢失，玩家可能高估技能稳定性。",
  "evidence_refs": []
}
```

### 5.4 白名单字段

#### `defect_class`

```text
semantic
terminology
presentation
style
technical
context
source
```

#### `phenomenon`

第一版至少包括：

```text
number
number-range
unit
condition
polarity
entity-role
scope
trigger-timing
omission
addition
terminology
proper-name
ambiguity
fluency
punctuation
register
voice
markup
format
runtime-key
alignment
source-problem
other
```

`other` 必须带解释，并进入 taxonomy gap 统计。

#### `meaning_change.type`

```text
omitted
added
weakened
strengthened
reversed
reassigned
made-ambiguous
presentation-only
none
unknown
```

#### 三态事实

所有影响事实使用：

```text
yes / no / unknown
```

不得把证据不足强制转换成 `no`。`unknown` 会触发人工裁决，不能自动派生 major。

#### `amplification_scope`

```text
local
repeated-context
cross-component
systemic
unknown
```

它影响审核优先级，不单独决定 severity。

### 5.5 逻辑一致性校验

宿主至少拒绝以下组合：

- `is_defect=no` 但 `is_substantive=yes`；
- `defect_class=presentation`、`meaning_change=presentation-only`，却声称
  `opposite_or_different_rule=yes` 且没有解释；
- `context_sufficient=false`，所有关键影响事实却均为确定的 `yes/no` 且无证据；
- source/target quote 无法在对应文本中定位；
- `occurrence` 越界；
- finding ID 重复、revision 缺失、字段未知或枚举非法；
- 模型输出宿主专属字段，如 `derived_severity`、`rule_id` 或 grade。

逻辑冲突不得静默修正，应使该 assessment 或对应 shard 校验失败。

## 六、证据 Span 规范化

### 6.1 不直接信任自由文本 span

模型输出短 `quote + occurrence`，宿主在原始 source/target 中解析为字符偏移：

```json
{
  "quote": "one of",
  "occurrence": 1,
  "start": 143,
  "end": 149
}
```

`start/end` 由宿主产生，不由模型产生。这样可以避免模型给出错误偏移。

### 6.2 漏译

漏译允许 `target_evidence.quote` 为空，但必须：

- 有非空 source quote；
- `meaning_change.type=omitted`；
- body 说明缺失内容在目标中的预期位置或语义角色。

### 6.3 整条问题

确实影响整条文本时，模型使用显式标记：

```json
{"quote": "", "occurrence": 0, "whole_item": true}
```

不得用复制完整长段落代替短证据。

### 6.4 Span 校验结果

规范化后记录：

```text
exact
ambiguous
missing
whole-item
```

只有 `exact` 或合法 `whole-item` 可自动进入问题匹配；其余进入人工队列。

## 七、问题单元身份与匹配

### 7.1 规范问题特征

宿主为每条 finding 生成：

```text
revision_id
normalized source span
normalized target span
phenomenon
error family
meaning_change.type
```

建议生成候选 `issue_key`：

```text
SHA256(
  revision_id,
  phenomenon,
  source_start,
  source_end,
  target_start,
  target_end,
  meaning_change.type
)
```

该 key 用于精确身份，但不能假设两个模型永远一对一拆分。

### 7.2 匹配必要条件

两个 finding 只有在以下条件下才可建立匹配边：

1. `revision_id` 相同；
2. source span 相交、相邻或都指向同一已知参数/术语；
3. phenomenon 相同，或属于 policy 明确声明的可合并组；
4. meaning change 不互相矛盾；
5. target span 若双方均非空，应相交、相邻或指向同一目标语义单元。

不得仅根据 title/body 文本相似度匹配。

### 7.3 可合并组示例

```text
number ↔ number-range
omission ↔ condition（当缺失内容就是条件）
terminology ↔ proper-name
fluency ↔ ambiguity（仅在 span 相同且 meaning change 兼容时）
```

可合并组必须版本化；匹配方向应对称。

### 7.4 图聚类而不是强制一对一

对同一 revision 的 finding 建立二部图：左侧 evaluator A，右侧 evaluator B。
满足匹配条件就连边，再按连通分量生成问题簇。

问题簇类型：

```text
full-match       一对一，证据和语义一致
partial-match    一对一，但 span 或 meaning change 只部分重合
split-merge      一对多或多对一
left-only        仅 A 报告
right-only       仅 B 报告
ambiguous        存在多个同等匹配，需人工确认
```

只有 `full-match`、`partial-match` 和人工确认后的 `split-merge` 才比较问题级影响事实。
未匹配 finding 进入发现集合差异统计，不能直接作为 severity 不一致。

### 7.5 规范 Issue ID

宿主按稳定排序为问题簇分配：

```text
QI-0001
QI-0002
...
```

并保存成员 finding ID，不覆盖模型原始 finding 身份。

## 八、Severity 派生规则

建议新增版本化文件：

```text
i18n/quality/impact-rules-v1.json
```

模型不得直接输出最终 severity。宿主只根据已经确认或双方一致的事实应用规则。
存在关键 `unknown` 或事实冲突时输出：

```text
derivation_state = needs-adjudication
```

### 8.1 Blocker

Blocker 主要来自确定性技术门禁，而不是模型主观判断：

- Lua/UTF-8/条目结构不可加载；
- printf 参数缺失或无法安全执行；
- 必要 markup/token 被破坏；
- 运行时键造成系统性错误。

模型可发现技术现象，但宿主必须用现有 lint/结构事实确认后才能派生 blocker。

### 8.2 Major

必须满足 `is_defect=yes`、`is_substantive=yes`，并命中至少一条 major 规则。
建议初始规则：

#### `S-RULE-01`：机制维度改变并影响决策

```text
mechanics_context=yes
AND changes_rule_understanding=yes
AND can_change_player_action=yes
AND phenomenon ∈ {
  number, number-range, unit, condition, polarity,
  entity-role, scope, trigger-timing
}
```

#### `S-OPER-01`：操作必要信息缺失

```text
required_operation_info_missing=yes
AND can_change_player_action=yes
```

#### `S-REVERSE-01`：相反或另一套规则

```text
opposite_or_different_rule=yes
AND changes_rule_understanding=yes
```

#### `S-FORMAT-01`：确定性运行破坏

由技术门禁确认，通常派生 blocker；若只影响单条显示但仍可运行，可按规则派生 major。

“数字、范围或条件出现错误”本身不自动等于 major。必须同时证明后果达到规则阈值。

### 8.3 Minor：实质问题

满足：

```text
is_defect=yes
AND is_substantive=yes
AND 未命中 major/blocker
```

典型情况：

- 有语义损失，但通常不改变操作或结果；
- 可从紧邻上下文恢复；
- 术语错误造成短暂理解困难，但不妨碍继续游戏；
- 叙事或风味文本存在局部事实偏差，但不影响游戏决策。

### 8.4 Minor：表达问题

满足：

```text
is_defect=yes
AND is_substantive=no
AND defect_class ∈ {presentation, style}
```

例如：

- 生硬、翻译腔或搭配错误；
- 明显标点、空格、排版问题；
- 语体或人物口吻不一致，但核心事实正确。

报告必须将“实质 minor”和“表达 minor”分开统计。

### 8.5 Note

满足：

```text
is_defect=no
```

表示可选优化或同样正确的表达偏好。note 不计入缺陷率。

### 8.6 派生输出

```json
{
  "derived_severity": "major",
  "derivation_state": "derived",
  "rule_id": "S-RULE-01",
  "supporting_facts": [
    "mechanics_context=yes",
    "changes_rule_understanding=yes",
    "can_change_player_action=yes",
    "phenomenon=number-range"
  ]
}
```

规则应用必须确定性、可单元测试，并在相同输入上逐字节重建。

## 九、两次阈值与缺陷类别

对外可以通俗地表达为两次阈值判断，但内部建议保存三个事实：

```text
is_defect
is_substantive
meets_major_rule（宿主派生，不由模型填写）
```

映射：

| is_defect | is_substantive | major rule | 结果 |
|---|---|---|---|
| no | 任意 | 否 | clean 或 note |
| yes | no | 否 | presentation/style minor |
| yes | yes | 否 | substantive minor |
| yes | yes | 是 | major |
| 技术门禁失败 | 任意 | 特殊规则 | blocker 或 major |

这样既保留现有 MQM 四级，又避免把“用词生硬”和“机制反转”放在同一事实轴上。

## 十、锚点案例

建议新增：

```text
i18n/quality/anchors-v1.json
```

### 10.1 锚点来源

- 只使用人工确认的校准集或历史裁决案例；
- 不使用封存验证集或正式 120 条；
- 每个边界 3–5 个锚点；
- 优先覆盖实际高争议模式，不堆积几十个示例；
- 锚点修改提升版本或 content hash，旧 assessment 不重解释。

### 10.2 锚点结构

```json
{
  "anchor_id": "S-NUM-01",
  "profile": "mechanics",
  "phenomenon": "number-range",
  "facts": {
    "changes_rule_understanding": "yes",
    "can_change_player_action": "yes",
    "recoverable_from_immediate_context": "no"
  },
  "derived_severity": "major",
  "rule_id": "S-RULE-01",
  "rationale": "浮动伤害被改成固定上限，可能改变技能选择。"
}
```

### 10.3 模型如何使用锚点

模型输出：

```text
closest_anchor_id
anchor_relation = below / comparable / meets / exceeds / unknown
```

锚点比较是事实判断的辅助信号，不能单独决定 severity。宿主仍按 impact facts 和规则派生。

### 10.4 建议初始锚点主题

- 数值或范围部分丢失；
- 必要条件被弱化或删除；
- 否定、主客体或触发时机改变；
- 术语错误但上下文可推断；
- 风味文本中的事实偏差；
- 机制文本中的轻度措辞变化；
- 意义正确但表达生硬；
- 标点和空格错误；
- 信息已在紧邻上下文完整出现的重复省略。

## 十一、数据集重新划分

### 11.1 探索回归集

现有 12 条 dry-run：

- 已经多次观察和调试；
- 永久标记为 exploratory；
- 可用于 schema、匹配和规则回归；
- 不再用于宣称模型泛化、一致性或达标。

### 11.2 校准集

建议 32 条，固定 seed：

```text
tome4-quality-calibration-v2
```

特点：

- 与现有 12 条、封存集和正式 120 条完全互斥；
- 边界案例富集；
- 覆盖 mechanics、UI、日志、术语、对话和叙事；
- 可反复查看、裁决和修改规则；
- contrast 组保持原子性。

建议边界构成：

| 主题 | 建议最少数量 |
|---|---:|
| 数字/范围/单位 | 4 |
| 条件/否定/对象/时机 | 6 |
| 术语与专名 | 4 |
| 可从上下文恢复的信息 | 4 |
| 叙事事实与风味细节 | 4 |
| 表达/标点/风格 | 6 |
| 技术结构 | 4 |

同一条可同时满足多个主题。

### 11.3 封存验证集

建议 32 条，固定 seed：

```text
tome4-quality-holdout-v2
```

要求：

- 与探索集、校准集、正式 120 条互斥；
- 分布尽量接近正式 120 条，而不是边界富集；
- 规则冻结前不查看模型结果；
- 预先规定每个模型只运行一次主评估；
- 未达标则记录失败并返回校准阶段，不能根据逐条答案修改后继续把同一集合称为封存验证。

如果需要新的封存验证，必须生成新的 seed/contract，并保留失败集及结果。

### 11.4 正式 120 条

现有正式 sample ID 和内容保持不变。不得因为发现争议样本而删除或替换条目。

可以提前运行 `discovery-only`，但必须满足：

- 使用独立 contract；
- 不生成正式 grade/severity；
- 不将输出用于修改 v2 规则或锚点；
- 不计入 M4 正式一致性；
- 正式评估必须在 v2 规则冻结后从头运行。

如果使用正式 120 条中的前 20–30 条调规则，这些条目就不能继续作为无偏正式 benchmark。
本方案因此优先使用独立校准集，而不是用正式样本调参。

## 十二、模型盲评协议

每个 evaluator 必须：

- 无工具、无会话、无 skills、无项目上下文；
- 只接收 bounded quality bundle；
- 不接收另一 evaluator 的 assessment；
- 不接收裁决、历史 finding、remediation、预期 grade 或质量门槛答案；
- 使用相同 rubric、impact rules、anchors 和 prompt 版本；
- 记录 provider、model、thinking 和全部 content hash；
- 缓存只按 evaluator/provider/model/thinking/prompt/rules/anchors/bundle 精确命中；
- 相同缓存结果不得伪装成第二次独立评价。

模型/provider 选择属于运行配置，不写死在规则中。每次首次外部传输仍按 `AGENTS.md`
取得授权；授权范围、provider、model、bundle 类型和条目数写入宿主运行记录。

## 十三、Bundle 分片与合并

正式 120 条不建议强制模型一次输出全部结果。为降低 JSON 截断、漏项和注意力衰减，
建议 evaluator bundle 分为不超过 20 条的 shard：

- 按 sample 稳定顺序切分；
- contrast group 不得拆分；
- 每个 shard 使用相同 prompt/rules/anchors；
- shard 之间不展示前一 shard 的结论；
- 每个 shard 严格校验完整性后才能进入合并；
- 全部 shard 通过后，宿主按正式 sample 顺序合并为一个 assessment；
- 任一 shard 失败时整个 evaluator assessment 保持 incomplete，不得把部分结果冒充完整评价。

合并身份建议：

```text
assessment_id = SHA256(
  sample_id,
  evaluator identity,
  ordered shard bundle_ids,
  ordered normalized items
)
```

分片不会把同一模型的多个调用算成多个 evaluator；它们共同构成一个 evaluator 的完整 assessment。

## 十四、匿名人工裁决

### 14.1 裁决输入

生成独立 dispute bundle，匿名展示：

- source、target 和必要上下文；
- 问题候选 X/Y，顺序按稳定 seed 打乱；
- 规范化 span、phenomenon 和 meaning change；
- 双方 impact facts；
- 适用规则和候选锚点。

默认不展示：

- provider/model；
- reviewer-a/reviewer-b；
- 哪一方给出更多 finding；
- 历史 grade 或预期结论。

provider/model 身份保留在单独审计 artifact 中，供事后方法分析，不进入首轮裁决界面。

### 14.2 裁决顺序

1. X/Y 是否描述同一个问题；
2. 问题是否真实存在；
3. 规范化 span 和 phenomenon 是否正确；
4. 哪些 impact facts 成立；
5. 宿主重新应用规则派生 severity；
6. 如果规则无法处理，标记 `rule-gap`，不得直接凭感觉绕过规则。

### 14.3 裁决记录

```json
{
  "issue_id": "QI-0007",
  "same_issue": true,
  "exists": true,
  "confirmed_facts": {
    "is_defect": "yes",
    "is_substantive": "yes",
    "changes_rule_understanding": "yes",
    "can_change_player_action": "yes",
    "recoverable_from_immediate_context": "no"
  },
  "derived_severity": "major",
  "rule_id": "S-RULE-01",
  "anchor_id": "S-NUM-01",
  "rationale": "遗漏最低伤害值，将浮动范围表达为固定高值，可能改变技能选择。"
}
```

`derived_severity` 必须能由 confirmed facts 和 rule ID 确定性重算；不一致时裁决校验失败。

### 14.4 回归集

满足以下条件的裁决案例可以进入版本化回归集：

- 两个模型有实质分歧；
- 人工已经确认事实和规则；
- 不包含绝对路径、凭据或越界上下文；
- 绑定 current revision 或明确标记为 synthetic anchor；
- 通过 schema 和规则重算。

修改 prompt、规则、匹配算法或模型组合后，应重新运行这些历史争议案例。
旧结果保留，不能覆盖。

## 十五、指标体系

### 15.1 条目级

- 任意实质缺陷存在与否的一致率；
- major/blocker 存在与否的一致率；
- clean/defect 混淆矩阵；
- context sufficient 一致率；
- profile 一致率。

### 15.2 问题发现级

- evaluator A/B finding 数量；
- finding 集合的交集、并集与 Jaccard；
- full/partial/split-merge/left-only/right-only/ambiguous 数量；
- issue matching 成功率；
- unmatched finding 比例；
- error family precision/recall/F1（互相比较，不冒充真值）。

### 15.3 匹配问题的事实级

逐字段报告：

- `is_defect` 一致率；
- `is_substantive` 一致率；
- 规则理解影响一致率；
- 玩家行动影响一致率；
- 操作必要信息缺失一致率；
- 上下文可恢复性一致率；
- `unknown` 比例；
- 锚点选择一致率。

### 15.4 对人工裁决真值

只有完成匿名人工裁决后才能报告：

- 每个 evaluator 的 major precision/recall；
- 两个 evaluator 并集的 major recall；
- major 漏判数和误报数；
- 双方都漏掉的 confirmed major 数；
- 规则派生 severity 的准确率；
- 需要人工裁决的 issue/条目比例。

不得把另一模型当成真值来计算“漏判率”。

### 15.5 稳定性

在校准集、固定 prompt 和固定规则上预先规定重复次数，报告：

- 同一模型重复运行 finding Jaccard；
- impact facts 重复一致率；
- derived severity 重复一致率；
- JSON/结构失败率；
- 缓存命中与真实新请求分开统计。

重复运行只用于方法稳定性，不增加某个 revision 的独立置信度。

### 15.6 κ 的位置

保留 severity weighted κ，但作为次要诊断指标，并同时报告原始混淆矩阵、样本量和置信区间。

κ 不单独决定系统是否可用。例如：

- 双模型并集没有漏掉 confirmed major；
- major 分歧均进入人工裁决；
- 普通语义 minor 和表达 minor 偶有混淆；
- 人工裁决比例可接受；

这种系统可能比“κ 较高但偶尔双方同时漏掉 major”的系统更适合质量控制。

## 十六、建议预注册验收指标

在运行封存验证集前冻结目标，禁止看结果后修改：

| 指标 | 建议目标 | 说明 |
|---|---:|---|
| assessment/schema 覆盖率 | 100% | 任一缺项均失败 |
| 实质缺陷存在一致率 | ≥80% | 与现有阶段目标一致 |
| major-or-worse 一致率 | ≥90% | 仍需结合样本中 major 数量解释 |
| 匹配问题关键 impact fact 一致率 | ≥80% | 分字段报告，不只给平均值 |
| taxonomy/phenomenon 无法映射 | <5% | `other` 和 rule-gap 均计入 |
| context/事实不足 | <10% | unknown 需要人工 |
| 双模型并集漏掉的 confirmed major | 0 | 以人工裁决为准 |
| 需要人工裁决的条目比例 | 建议 ≤30% | 超出则暂不扩展规模 |
| severity weighted κ | 目标 ≥0.70 | 次要门槛，不单独决定 Go/No-Go |

如果封存集中 confirmed major 数量过少，应明确报告“证据不足”，不能用 100% 比例宣称稳定。

### 16.1 决策结果

- **Go**：关键目标达成，进入正式 120 条；
- **Go with human severity**：问题发现可靠、major 并集无漏判，但 severity/事实仍需较多人工裁决；
- **Exact-only**：适合构建经人工确认的精确质量库，不支持自动模糊复用；
- **No-Go**：问题身份、事实一致性或 major 漏判不可接受，返回规则和上下文设计。

## 十七、格式与传输失败处理

格式错误与翻译判断质量分开统计。

### 17.1 必须保存

```text
raw-output.txt
parsed-output.json（成功解析时）
repaired-output.json（发生确定性语法修复时）
assessment.json（严格校验后的宿主 envelope）
pi-quality-evaluator.json
```

报告字段：

```json
{
  "syntax_auto_repaired": true,
  "repair_rule": "missing-final-outer-brace-v1",
  "raw_output_sha256": "...",
  "repaired_output_sha256": "..."
}
```

### 17.2 允许的自动修复

只允许有形式证明、不改变语义内容的有限规则，例如：

- 完整、可解析的 `items` 数组仅缺最外层最后一个 `}`；
- 宿主补齐自己拥有的 deterministic envelope。

每种修复规则必须：

- 有独立版本号；
- 有正反单元测试；
- 保留原始字节和修复后字节；
- 修复后仍通过完整 schema、ID、覆盖和语义字段校验。

### 17.3 必须拒绝

- 缺条目、重复 revision、顺序错乱；
- finding 缺字段或枚举非法；
- JSON 内容截断；
- 模型输出宿主专属 severity/grade 并试图覆盖规则；
- 无法唯一确定的括号、引号或转义修复；
- 第三个模型自由重写或“修复” JSON。

### 17.4 重试

正式评估默认不做语义重试。格式失败时：

- 若可确定性修复，按规则修复并标记；
- 否则该 shard 失败；
- 重新调用同一 evaluator 视为新的 attempt，保留失败原始输出；
- 不从多次结果中挑选更符合预期的一次；
- 预注册允许的最大重试次数，并在报告中单独统计。

## 十八、安全与授权边界

- evaluator 保持 `--no-tools --no-session --no-context-files --no-skills`；
- bundle 只包含 sample packet、规则摘要和锚点，不附绝对路径；
- 不向模型发送 `.artifacts` 中的其他 assessment、裁决或缓存；
- provider/model 调用前按 `AGENTS.md` 报告 bundle 类型、数量和条目数并取得授权；
- 授权只覆盖明确的 provider、model、数据类型和会话/任务范围；
- 原始模型输出和未裁决结果只留在 `.artifacts/i18n/quality/`；
- 不自动写规范 Lua、术语表或发布仓库；
- 模型 assessment 不替代人工机制核验；
- 公开源码证据和 DLC 输入继续遵守项目现有边界。

## 十九、建议目录与 Contract

### 19.1 版本控制

```text
i18n/quality/
  rubric-v2.md
  impact-rules-v1.json
  anchors-v1.json
  policy-v2.json
  schemas/
    assessment-v2.schema.json
    issue-cluster-v1.schema.json
    dispute-v1.schema.json
    adjudication-v2.schema.json
  regressions/
    disputed-cases-v1.jsonl

i18n/prompts/
  pi-quality-evaluator-v2.md
```

是否把具体裁决案例写入版本控制，仍需通过内容边界、许可证和 schema 审核。

### 19.2 派生 artifact

```text
.artifacts/i18n/quality/
  runs/<run>-calibration-v2/
  runs/<run>-holdout-v2/
  runs/<run>-evaluator-shard/
  runs/<run>-issue-match/
  runs/<run>-dispute/
  runs/<run>-adjudication-v2/
  runs/<run>-report-v2/
```

### 19.3 建议 contract

```text
tome4-quality-assessment-v2
tome4-quality-impact-rules-v1
tome4-quality-anchors-v1
tome4-quality-issue-cluster-v1
tome4-quality-dispute-v1
tome4-quality-adjudication-v2
tome4-quality-report-v2
```

## 二十、建议 CLI

保持 `tools/i18n` 为本地确定性入口，Pi runner 只执行外部 evaluator：

```bash
# 生成互斥校准/封存集
python3 -B tools/i18n quality calibration \
  --inventory <inventory.jsonl> \
  --calibration-size 32 \
  --holdout-size 32

# 构建 evaluator shards，不联网
python3 -B tools/i18n quality evaluator-bundles \
  --sample <sample.json> \
  --evaluator reviewer-a \
  --max-items 20

# 经授权后运行单个模型 evaluator
python3 -B tools/pi-quality-evaluator \
  --sample <sample.json> \
  --evaluator reviewer-a \
  --provider <provider> \
  --model <model> \
  --thinking <level>

# 规范化和匹配两个完整 assessment
python3 -B tools/i18n quality match \
  --sample <sample.json> \
  --assessment <reviewer-a.json> \
  --assessment <reviewer-b.json>

# 生成匿名争议 bundle
python3 -B tools/i18n quality disputes \
  --match <issue-match.json>

# 校验裁决并派生 severity
python3 -B tools/i18n quality adjudicate-v2 \
  --match <issue-match.json> \
  --adjudication <adjudication-v2.json> \
  --strict

# 生成 v2 报告
python3 -B tools/i18n quality report-v2 \
  --validation <validation-v2.json>
```

CLI 名称可在实现时微调，但 contract、离线/联网边界和 artifact 语义不得改变。

## 二十一、实施里程碑

### M4a：冻结 v2 决策

- 确认事实字段、三态值、phenomenon 白名单；
- 确认 severity 派生规则和传播风险分离；
- 确认 32+32 数据划分与正式 120 条隔离；
- 确认匿名裁决流程。

完成条件：没有需要 evaluator 临时发明的字段或 severity 规则。

### M4b：Schema、规则和单元测试

- 新增 assessment-v2、issue cluster、dispute、adjudication-v2 schema；
- 实现 impact rule engine；
- 实现逻辑冲突校验；
- 为每条规则增加正例、反例和 unknown 测试；
- 保证 v1 artifact 仍可按旧逻辑读取。

完成条件：相同 facts 必定派生相同 severity；未知/矛盾事实不会被静默降级。

### M4c：问题规范化与匹配

- 实现 quote→offset；
- 实现可合并 phenomenon；
- 实现二部图与 split/merge cluster；
- 生成稳定 issue ID；
- 增加拆分/合并/歧义回归测试。

完成条件：已裁决 fixture 的问题簇可确定性重建，匹配不依赖标题文本相似度。

### M4d：校准集与锚点

- 从 inventory 生成 32 条互斥校准集；
- 双模型盲评并匿名人工裁决；
- 形成每个主要边界 3–5 个锚点；
- 冻结 rubric/prompt/rules/anchors hash；
- 在冻结配置下预注册并执行模型内稳定性测试。

完成条件：规则和锚点可以覆盖主要争议，rule-gap 与 unknown 比例可接受。

### M4e：封存验证

- 生成并封存 32 条近正式分布样本；
- 记录预注册指标和运行次数；
- 两个 evaluator 各完成一次主盲评；
- 匿名裁决所有 major 候选和关键分歧；
- 输出 Go/Go with human severity/Exact-only/No-Go。

完成条件：未查看结果前已冻结所有规则；报告不挑选单次最优运行。

### M4f：正式 120 条

- 仅在 M4e 允许后启动；
- 使用冻结 v2 方法从头盲评；
- 保存全部 shard 原始输出；
- 规范化、匹配、匿名裁决；
- 生成正式 v2 assessment/adjudication/report。

完成条件：120 条完整覆盖，没有未决 major、悬空 issue 或无法重算的 severity。

## 二十二、测试计划

### 22.1 Schema 和身份

- 模型不能输出宿主 severity/rule/grade；
- provider/model/prompt/rules/anchors hash 由宿主固定；
- revision、finding、shard 和 assessment ID 完整唯一；
- shard 合并顺序必须与 sample 一致；
- v1/v2 contract 不互相误读。

### 22.2 Span

- 唯一 quote 正确解析 offset；
- 重复 quote 必须提供合法 occurrence；
- 漏译 target 空 span 合法但受额外约束；
- whole-item 不能携带完整长段落副本；
- 不存在或越界 quote 被拒绝。

### 22.3 规则

- `3–8`→`8` 在 mechanics 且影响选择时派生 major；
- 叙事中的时间范围弱化但不影响操作时派生 substantive minor；
- 上句已完整给出、下句重复省略时不自动 major；
- 标点错误派生 presentation minor；
- 可选表达偏好派生 note；
- systemic 传播风险不单独把 presentation minor 升为 major；
- 关键事实 unknown 时进入 needs-adjudication。

### 22.4 匹配

- 相同问题一对一 full match；
- 一条总 finding 对两条细 finding 形成 split-merge；
- 同 revision 不同 span 不错误合并；
- 可合并 error family 对称；
- body 标题相似但证据不同不匹配；
- ambiguous cluster 进入人工队列。

### 22.5 盲评和安全

- bundle 不含另一 assessment、裁决、历史 finding 或 expected grade；
- Pi 命令无 tools/session/context/skills；
- bundle 内容不含主机绝对路径；
- 缓存命中不产生外部传输；
- 两个 evaluator 缓存命名空间分离；
- 外部授权信息写入宿主报告。

### 22.6 格式

- 唯一允许的缺右花括号修复成功并双 hash；
- 截断 items、缺字段、重复 ID、顺序错误全部拒绝；
- raw/repaired/assessment 内容身份可验证；
- 重试不会覆盖首次失败 artifact。

## 二十三、迁移与兼容

1. 保留当前 v1 taxonomy、policy、rubric、assessment 和 report；
2. 现有 12 条同会话 dry-run 和双模型盲测结果继续作为历史 artifact；
3. 不用 v2 规则重新计算并覆盖 v1 severity；
4. 如需比较，只在报告中并列显示“v1 模型标签”和“v2 规则派生”，明确方法不同；
5. 正式 benchmark 只有在 v2 封存验证和人工批准后才进入版本控制；
6. v2 失败可删除派生 artifact 回滚，不触碰规范 Lua 或术语表。

## 二十四、当前建议

采纳本方案，但暂不把现有两个模型宣布为“已校准的正式 evaluator”。它们当前适合作为：

- 独立问题发现器；
- impact facts 候选提供者；
- 人工争议队列的召回来源。

下一步不是继续重跑原 12 条，而是先实现 v2 schema、规则引擎和问题匹配，再生成与正式
120 条互斥的 32 条校准集和 32 条封存集。只有冻结配置在封存集上通过预注册检查后，
才开始正式 M4 双评。

最终成功标准不是两个模型在所有三级标签上完全一致，而是：

- 严重问题不会被两个模型共同漏掉；
- 普通语义问题与表达问题可以解释和区分；
- 每个 severity 都能从事实、规则和锚点重算；
- 所有分歧都能进入匿名、可追踪的裁决流程；
- 随着裁决案例积累，rule-gap 和人工裁决比例持续下降。
