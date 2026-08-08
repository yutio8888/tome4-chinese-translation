# ToME4 翻译质量评价与可复用译文库整体方案

> 状态：设计草案 v0.1。第一阶段（质量清单与校准试点）的 M0–M3 已实现：
> v1 inventory/sample/validate/report 与 12 条探索盲测已落地；Evaluator v2 离线契约、规则引擎、问题匹配、匿名裁决、32+32 数据准备、分片、fake runner 和报告已于 2026-08-06 完成。presentation-only 漂移已改为宿主确定性 scope；新 lineage 复测中 Luna 两次 finding Jaccard 与两模型有效主跑交叉 Jaccard 均为 1.000，但 DeepSeek 强制复跑未产生 final answer，按预注册不可替换，M4d 仍为 No-Go。封存验证、正式 120 条、M5 裁决与 M6 Go/No-Go 均未启动。2026-08-07 离线闭环：共享 claim/contract 核心（quality_contracts/quality_claims，legacy v2/v3/Facts 与 canonical-v1 四 profile）、版本化 dataset-registry-v1（8 登记项/276 revision）、curation v1 数据流（80 条 source-side 候选池已真实构建，五 stratum 达标并显式报告 ui 长度 relaxation）与 15 个完整嵌套 schema 已落地；五个隔离角色（Facts/curator/Gold A/B/adjudicator）执行停在外部授权边界之前，33-slot fake replay 与 report v2 已通过 fixture 集成验证。
> 适用范围：本仓库中的规范中文译文、术语库以及由它们生成的翻译记忆和联想索引。
> 第一阶段实施方案见 [`translation-quality-phase-1.md`](./translation-quality-phase-1.md)；
> AI evaluator 的事实判定、问题匹配、规则定级和匿名裁决 v2 方案见
> [`translation-quality-evaluator-v2.md`](./translation-quality-evaluator-v2.md)。

## 一、背景与目标

当前项目已经具备以下基础：

- 规范 Lua 译文及基于 LuaJIT 的语义加载器；
- `lint --strict` 对空译文、printf 参数、控制标记和组件内运行时键冲突的检查；
- `terminology.tsv` 的 `existing / review / preferred` 术语状态和上下文信息；
- 跨组件运行时键扫描、重复键分类和构建验证；
- 内容寻址的 review bundle、结构化 finding、remediation proposal 与人工裁决记录；
- 固定游戏版本、源码 commit 和提取快照的 manifest。

这些能力可以证明“译文结构是否安全”“某些问题是否已经被发现和处置”，但尚不能直接回答：

1. 当前这一个 target 的语义和中文质量如何；
2. 该结论绑定的是不是当前 target，而非历史版本；
3. 结论有多少独立证据；
4. 该译文能否用于精确匹配、模糊匹配或片段联想；
5. 复用后是否会把原有问题扩散到更多文本。

本方案的目标是建立一套可解释、可复现、可校准的质量系统，用于：

- 筛选可信的整句译文、格式模板和规范术语；
- 形成可重新生成的高质量翻译记忆；
- 为后续精确匹配、模糊匹配和上下文联想提供质量与适用范围信号；
- 将审核、修订、源码核验和实际使用反馈沉淀为可追踪证据；
- 在原文、译文、术语或游戏版本变化时自动使旧认证失效。

### 非目标

- 不把当前全部规范 Lua 自动视为高质量参考答案；
- 不以 BLEU、COMET、语言模型打分或“没有 finding”作为单独认证依据；
- 不让质量工具或模型直接修改规范 Lua；
- 不在第一阶段实现自动翻译、自动应用建议或完整模糊搜索服务；
- 不用一个不透明总分取代错误证据和人工裁决。

## 二、核心设计原则

### 2.1 三轴分离

每个译文 revision 必须分别给出三个结论：

1. **质量（quality）**：它在当前出现位置是否正确、完整、自然；
2. **置信度（confidence）**：现有证据足以支持该结论到什么程度；
3. **复用性（reusability）**：它可以在哪些上下文中安全复用。

高质量不等于高复用性。例如，人物对白可以在原场景中非常优秀，但只能精确复用；简短规范术语则可能适合跨文件复用。

### 2.2 先门禁，后分级

Lua、格式参数、控制标记、运行时冲突和未解决严重错误属于资格门禁。门禁失败的译文不能通过其他维度的高分抵消。

### 2.3 所有证据绑定具体 revision

审核结论不得只绑定 source 或逻辑条目。target、`args_order`、`special`、相关版本中任一项变化后，旧审核只能作为历史记录，不能继续认证新 revision。

### 2.4 上下文优先于表面相似度

质量判断和检索都必须保留 component、section、`source_tag`、文本功能、游戏领域和结构签名。不能把 `source → target` 当作无条件全局映射。

`light / entity subtype` 的既有裁决说明：表面词义、源码语境和运行时键约束可能互相冲突，最终结论必须同时考虑实际运行行为和复用边界。

### 2.5 可解释、可校准、可撤销

每次降级、晋级或隔离都应能追溯到具体门禁、MQM 错误、裁决或版本变化。规则和模型必须在人工标注基准集上校准；错误晋级应可回滚。

### 2.6 规范数据与派生数据分离

- 规范 Lua 仍是整句译文的唯一内容源；
- `terminology.tsv` 仍是术语裁决的唯一内容源；
- 版本控制中只保存质量规则、严格校验过的人工裁决和基准集；
- 全量清单、评分报告、候选库和检索索引均为可重建 artifact；
- 模型原始输出和未裁决候选不得直接进入权威质量数据。

## 三、评价对象和文本类型

### 3.1 三类评价对象

| 对象 | 说明 | 默认复用方式 |
|---|---|---|
| 术语 | 专名、资源、伤害、状态、技能等规范映射 | 按 category/domain/source_tag/scope 约束复用 |
| 整句或完整段落 | 一个 canonical `t(...)` 翻译 revision | 精确匹配或上下文兼容的模糊联想 |
| 格式模板 | 含 printf、颜色、token 等结构的完整模板 | 结构签名完全兼容后复用 |

不得从一条高质量长句自动推导其任意子串也是高质量译法。可复用片段必须通过单独的术语或人工对齐流程进入库。

### 3.2 文本功能 profile

`domain` 表示内容领域，profile 表示文本的交际功能，两者不能混用。第一版建议使用：

| profile | 典型内容 | 评价重点 |
|---|---|---|
| `mechanics` | 技能、效果、物品机制说明 | 准确性、条件、数字、机制事实 |
| `term-name` | 技能名、职业、实体、专名 | 术语、专名一致性、简洁性 |
| `ui` | 菜单、按钮、标签、提示 | 操作含义、长度、实际呈现 |
| `runtime-log` | 战斗日志、系统消息 | 主客体、参数角色、时态、可扫读性 |
| `dialogue` | 对话、选项、角色发言 | 指代、人物口吻、自然度 |
| `narrative` | lore、剧情、成就描述 | 完整性、文体、世界观一致性 |
| `technical-internal` | 调试、内部键、技术文本 | 结构安全、是否确实玩家可见 |
| `unknown` | 自动分类证据不足 | 必须补充上下文，不能晋级 Gold |

profile 可以由 `source_tag`、section 和术语 category 推断，但必须允许有证据的人工覆盖。自动分类置信度不足时宁可保留 `unknown`。

## 四、MQM 风格错误体系

本项目采用“MQM 启发式”而非宣称完全实现某一外部 MQM 版本。核心做法是：对具体 revision 记录错误位置、类型、严重程度、证据和裁决状态，再从已裁决错误生成质量结论。

### 4.1 第一版错误分类

| 一级类别 | 建议错误代码 | 含义 |
|---|---|---|
| 准确性 | `ACC_MISTRANSLATION` | 一般错译 |
|  | `ACC_OMISSION` | 漏译有效信息 |
|  | `ACC_ADDITION` | 无依据增译 |
|  | `ACC_UNTRANSLATED` | 应翻译内容残留英文或占位文本 |
|  | `ACC_POLARITY` | 否定、肯定、增减方向反转 |
|  | `ACC_CONDITION` | 条件、例外、范围、时序或比较关系错误 |
|  | `ACC_NUMBER_UNIT` | 数字、概率、回合、距离、单位错误 |
|  | `ACC_ENTITY_ROLE` | 施法者、目标、主客体、指代对象错位 |
|  | `ACC_MECHANICS` | 与固定版本实际游戏机制不符 |
| 术语 | `TERM_PREFERRED` | 未采用适用的 preferred 术语且无例外证据 |
|  | `TERM_PROPER_NAME` | 人名、地名、组织等专名错误 |
|  | `TERM_INCONSISTENT` | 同一适用上下文中无理由多译 |
| 中文流畅度 | `FLU_GRAMMAR` | 语法错误 |
|  | `FLU_WORD_CHOICE` | 搭配或用词不当 |
|  | `FLU_AWKWARD` | 生硬、欧化、冗余但含义基本可辨 |
|  | `FLU_AMBIGUITY` | 中文引入原文没有的歧义 |
|  | `FLU_PUNCTUATION` | 标点、空格和中文排版问题 |
| 风格 | `STYLE_REGISTER` | 语体不符合文本功能 |
|  | `STYLE_VOICE` | 人物口吻或称谓不一致 |
|  | `STYLE_NARRATIVE` | 叙事风格和世界观表达不一致 |
| UI/呈现 | `UI_CLARITY` | 按钮、标签或提示不清楚 |
|  | `UI_LENGTH` | 明显过长或截断风险 |
|  | `UI_RENDER` | 换行、颜色或动态渲染后不可读 |
| 技术 | `TECH_FORMAT` | printf 数量、类型、宽度或精度问题 |
|  | `TECH_ARGS_ORDER` | 参数顺序或参数语义角色错误 |
|  | `TECH_MARKUP` | 颜色、富文本等标记错误 |
|  | `TECH_TOKEN` | `@token@` 缺失、大小写或数量错误 |
|  | `TECH_LUA` | Lua 字面量、编码或加载问题 |
|  | `TECH_RUNTIME_KEY` | 运行时键覆盖或冲突风险 |
| 上下文 | `CTX_SOURCE_TAG` | 使用了错误 `source_tag` 语境的译法 |
|  | `CTX_DOMAIN` | 使用了错误领域或类别的译法 |
|  | `CTX_ALIGNMENT` | 原文与译文条目错位、复制错段 |
|  | `CTX_INSUFFICIENT` | 现有上下文不足以形成可靠结论 |
| 目录/版本 | `CATALOG_DUPLICATE` | 不合法重复或冲突声明 |
|  | `CATALOG_STALE` | 对应旧原文、旧机制或旧术语依赖 |
| 原文问题 | `SOURCE_AMBIGUOUS` | 原文自身有歧义，暂不归责于译文 |
|  | `SOURCE_INCORRECT` | 原文与实际机制不符，译文存在有证据的修正 |

`SOURCE_*` 用于记录评价限制和有意偏离，不直接计为译文缺陷，但会影响置信度和复用范围。

### 4.2 严重程度

| severity | 判定标准 | 示例 |
|---|---|---|
| `blocker` | 译文不可运行、破坏格式或会造成系统性错误 | Lua 加载失败、参数缺失、关键 token 损坏 |
| `major` | 实质改变含义、机制或玩家决策 | 伤害类型错误、否定反转、关键条件遗漏 |
| `minor` | 确有问题，但不改变核心机制和主要决策 | 局部生硬、次要术语不一致、明显标点问题 |
| `note` | 非缺陷的可选优化 | 两种表达均正确时的风格建议 |

`note` 不计入缺陷分。任何 finding 在人工裁决前都只是 observation；只有 `confirmed` 或 `partially_confirmed` 的当前 revision finding 才能影响最终等级。

### 4.3 文本跨度与证据

每个错误应尽可能记录：

- source/target 中的短跨度或参数位置；
- 错误代码和严重程度；
- 简洁、可复核的理由；
- 适用术语行、固定源码 commit、运行时截图或其他证据引用；
- `proposed / confirmed / partially_confirmed / rejected / resolved` 状态；
- 绑定的 `revision_id`。

不得通过复制完整受限上下文来证明一个局部错误。公开机制核验按项目现有规则记录组件、相对路径、固定 commit 和关键行为。

## 五、质量结论模型

### 5.1 技术和严重错误门禁

建议定义以下门禁组：

| gate | 通过条件 |
|---|---|
| `QG_LOAD` | UTF-8、LuaJIT 加载和条目结构有效 |
| `QG_NONEMPTY` | target 非空，且不含未裁决占位翻译 |
| `QG_FORMAT` | printf、`args_order` 和参数语义角色已验证 |
| `QG_MARKUP` | markup、`@token@`、换行等差异相同或已裁决 |
| `QG_RUNTIME` | 组件内及跨组件运行时键没有未解决冲突 |
| `QG_CURRENT` | 证据绑定当前 version 和当前 revision |
| `QG_SEVERE` | 没有未解决的 confirmed blocker/major |
| `QG_CONTEXT` | profile、source_tag 和必要上下文已确定 |
| `QG_TERMS` | 相关 preferred 术语一致，或存在明确例外裁决 |

门禁可以是 `pass / fail / needs-review / not-applicable`。只有全部适用门禁为 `pass` 才有资格进入正式翻译记忆。

### 5.2 多维质量向量

门禁通过后，按 0–4 或 `not-applicable` 保存以下维度：

```text
accuracy
mechanics_context
terminology
fluency
style
ui_render
corpus_consistency
```

建议含义：

- `4`：已针对该维度核验，无实质问题；
- `3`：正确，仅有不计缺陷的可选优化；
- `2`：基本可用，但上下文或证据不足；
- `1`：存在 confirmed minor 或局部重要问题；
- `0`：存在 confirmed major/blocker；
- `null`：该维度不适用。

第一阶段不发布统一加权总分。后续如需要排序，只能在相同 profile 内、基于人工基准校准权重；原始向量和错误记录必须始终保留。

### 5.3 证据置信度

| 等级 | 最低证据 |
|---|---|
| `C0` | 未检查或 revision 已变化 |
| `C1` | 当前 revision 仅通过确定性自动门禁 |
| `C2` | 一次完整、可追踪的语义评估，且上下文充分 |
| `C3` | 针对完整条目的人工裁决，或两次真正独立且经过校准的评估一致 |
| `C4` | C3 基础上完成必要的源码机制、运行时呈现或第二位人工审核验证 |

置信度是证据强度，不是语言质量分。缓存重放、相同模型同提示的重复运行和仅处理既有 finding，不自动构成独立完整评估。

### 5.4 质量等级

| grade | 条件 | 使用方式 |
|---|---|---|
| `Gold` | 全部门禁通过；无未解决 confirmed 缺陷；通常要求 C3 以上；适用范围明确 | 正式高质量翻译记忆，可参与精确和受限模糊联想 |
| `Silver` | 全部门禁通过；无未解决 confirmed 缺陷；至少 C2 | 带证据提示的候选，默认不自动填充 |
| `Candidate` | 自动门禁通过，但语义评估不足或尚未裁决 | 仅进入审核队列，不进入普通用户联想结果 |
| `Quarantine` | 任一门禁失败、存在 confirmed 缺陷、版本过时或语境冲突 | 从检索索引排除 |

`Deprecated` 是生命周期状态，不是质量等级：旧 revision 即使曾经是 Gold，被新 revision 取代后也应保留历史但不参与当前检索。

### 5.5 复用范围

| reuse scope | 含义 |
|---|---|
| `general` | 在明确 locale/version/scope 内可广泛复用，通常只适合规范术语和极稳定标签 |
| `same-domain` | 仅在相同 domain/category/profile 中复用 |
| `same-tag` | 还必须匹配 `source_tag` 和结构签名 |
| `exact-context` | 仅限原 component/section 或相同运行键 |
| `no-reuse` | 双关、强角色口吻、来源问题或上下文不足，不进入联想 |

复用范围必须显式保存，不能仅由 Gold/Silver 推导。

### 5.6 风险优先级与质量分离

审核优先级建议使用独立风险模型：

```text
review_priority = defect_likelihood × impact × player_exposure × reuse_amplification
```

高频 UI、核心技能说明和即将被大量复用的候选应优先审核，但高影响或高频本身不能提高质量等级。

## 六、身份、版本和证据绑定

### 6.1 两层身份

沿用现有 `stable_entry_id` 的思路，区分：

- `unit_id`：标识 editorial unit，至少由 version 范围外的 component、section、source、`source_tag` 构成；
- `revision_id`：标识具体译文 revision，由 schema、游戏版本、`unit_id`、target、`args_order`、`special` 计算规范 JSON SHA-256。

行号和 ordinal 只作为位置元数据，不应成为长期 revision 身份，以免单纯重排使全部认证失效。若同一 editorial key 存在多个合法 occurrence，应保存 occurrence 列表，不用不稳定行号制造伪身份。

建议规范身份示意：

```json
{
  "identity_contract": "tome4-translation-revision-v1",
  "version": "tome-1.7.6",
  "unit_id": "...",
  "target": "...",
  "args_order": null,
  "special": null
}
```

### 6.2 结构签名

每个 revision 应保存或可重建：

- source/target printf token 的原始序列和 conversion 序列；
- 经 `args_order` 解释后的参数角色顺序；
- markup 和 `@token@` 多重集合；
- 换行数量和必要的模板形状；
- 数字、单位、否定词等高风险特征，供模糊匹配提示使用。

“归一化 source”只用于检索，不能取代原始 source 或结构签名。

### 6.3 依赖摘要

质量记录应绑定：

- manifest/version 摘要；
- canonical translation revision；
- 与该条目实际相关的术语行及摘要；
- 审核方法、规则版本、provider/model/prompt（如使用模型）；
- 必要时的源码 commit、提取快照或运行时验证证据。

长期实现应优先记录“相关术语依赖”，避免术语表中无关行变化导致全部质量记录失效；同时保留全表摘要用于审计。

## 七、数据分层和建议目录

### 7.1 权威输入

| 数据 | 权威来源 |
|---|---|
| 整句译文 | 规范 Lua |
| 术语 | `terminology.tsv` |
| 游戏版本和源码基线 | `i18n/versions/*.json` |
| 技术门禁规则 | `i18n/policy.json` 及质量 policy |
| 人工质量裁决 | 严格校验后的 quality assessment/benchmark 数据 |

### 7.2 建议的版本控制数据

后续实现阶段建议增加：

```text
i18n/quality/
  README.md
  taxonomy-v1.json
  policy-v1.json
  schemas/
    inventory-v1.schema.json
    assessment-v1.schema.json
    adjudication-v1.schema.json
  benchmarks/
    pilot-v1.jsonl
```

只有人工确认并通过严格 schema、revision 和来源校验的数据才能写入该目录。未经裁决的模型输出仍留在 `.artifacts`。

### 7.3 派生 artifact

```text
.artifacts/i18n/quality/
  runs/<timestamp>-inventory/
  runs/<timestamp>-sample/
  runs/<timestamp>-report/
  indexes/
  exports/
```

全量 inventory、候选等级、SQLite/JSONL/TMX 导出和搜索索引都应可由权威输入重新生成，不在规范 Lua 中嵌入评分字段。

## 八、评价与晋级工作流

```text
规范 Lua + manifest + terminology
              │
              ▼
      生成 revision inventory
              │
              ▼
   自动门禁、profile、风险特征
              │
              ├── fail ──> Quarantine
              │
              ▼
      有界、独立的语义评价
              │
              ▼
       finding 人工裁决
              │
              ▼
  质量向量 + confidence + reuse scope
              │
              ├── Candidate
              ├── Silver
              └── Gold
              │
              ▼
      生成精确 TM / 模糊索引
              │
              ▼
     采纳、编辑、拒绝和缺陷反馈
              └──────────> 再校准/降级/复审
```

### 8.1 晋级规则

- 自动 lint 只能晋级到 `Candidate/C1`；
- 模型无 finding 最多提供一次评估证据，不能单独晋级 Gold；
- finding 被修复后必须针对新 revision 重新执行至少相关门禁；
- 只有完整审核当前 revision，才能将历史 remediation 证据转化为当前置信度；
- 术语为 preferred 不代表包含该术语的整句自动合格；
- 人工有意偏离原文或术语时必须记录适用范围和证据。

### 8.2 自动降级和失效

以下事件触发重新计算：

- source、target、`source_tag`、`args_order` 或 `special` 改变；
- manifest 游戏版本或相关源码基线改变；
- 相关 preferred 术语发生变化；
- 新增 confirmed finding 或运行时冲突；
- 实际使用中发现回归问题。

旧 revision 保留历史 grade 和证据，但状态改为 `Deprecated`，不进入当前索引。

## 九、可复用译文库

### 9.1 分层库

建议将检索对象分开：

1. **术语库**：仅使用适用的 preferred 条目及明确别名；
2. **Gold 整句库**：正式检索主库；
3. **Silver 整句库**：带警告的辅助候选；
4. **格式模板库**：结构签名完全兼容的完整模板；
5. **人工片段库**：以后单独建立，不从整句自动切分；
6. **隔离/历史库**：仅用于审计和回归，不参与普通联想。

内部格式应优先使用保留完整元数据的 JSONL 或 SQLite；TMX 只能作为互操作导出，不能成为权威数据源。

### 9.2 精确匹配顺序

建议按以下优先级返回：

1. 同 `unit_id` 的当前 Gold revision；
2. 相同运行键、component 和版本的 Gold revision；
3. 相同原始 source、`source_tag`、profile/domain 和结构签名；
4. 相同 source 但存在多个语境译法时，返回带条件的 variants，不选全局默认；
5. Silver 只作为明确标注的后备候选。

### 9.3 模糊匹配流程

模糊匹配必须先过滤、后排序：

**硬过滤或强约束：**

- locale 和版本适用；
- printf 参数类型、数量和模板结构兼容；
- markup、token 和特殊选项兼容；
- `source_tag`、profile、domain/category 不冲突；
- 候选不处于 Quarantine/Deprecated。

**候选排序信号：**

- 字符、词、n-gram 或编辑距离相似度；
- 语义相似度；
- 上下文和术语重合度；
- Gold/Silver、confidence 和复用范围；
- 历史采纳后的编辑距离和缺陷记录。

**高风险差异惩罚：**

- 否定、比较、上下限、先后顺序；
- 数字、百分比、单位、持续时间；
- 伤害类型、资源、状态和专名；
- 施法者/目标角色；
- 条件从句的增加或删除。

质量等级只能改善合格候选的排序，不能覆盖上下文或结构不兼容。初期只展示 Top-K 建议、差异和证据，不自动写入 proposal 或规范 Lua。

## 十、系统评价指标

### 10.1 语料质量指标

- 当前 revision 自动门禁通过率；
- `C0–C4` 审核覆盖率；
- Gold/Silver/Candidate/Quarantine 覆盖率；
- 按 profile/domain/component 统计的 confirmed blocker/major/minor 密度；
- preferred 术语适用率和已裁决例外率；
- 同键冲突数、同源变体熵和无说明多译数；
- 因译文、版本或术语变化而失效的 stale 比例。

风险增强样本和总体代表性样本必须分开报告，不能用风险样本的缺陷率宣称全语料缺陷率。

### 10.2 评价系统指标

- 评审者对“是否有实质缺陷”的一致率；
- major-or-worse 判定一致率；
- 错误类别匹配 F1 和严重程度加权一致性；
- 自动规则和模型 finding 的 precision/recall；
- `CTX_INSUFFICIENT` 和无法归类错误的比例；
- confirmed/rejected finding 比例及不同方法的校准情况。

### 10.3 检索系统指标

- Gold 候选 `Precision@K`、`Recall@K`；
- Top-1/Top-3 人工可接受率；
- 采纳后的字符/词级编辑距离；
- 直接采纳、修改采纳和拒绝比例；
- 复用后被确认的 major/minor 逃逸缺陷率；
- 错误候选由上下文、结构还是质量信号导致的归因分布。

采纳率本身不是质量证明；盲目接受会造成虚高。应以复核后的编辑量和逃逸缺陷率作为更强指标。

## 十一、与现有工具链的关系

| 现有能力 | 在质量系统中的角色 | 不能单独证明的内容 |
|---|---|---|
| `lint --strict` | `QG_LOAD/QG_FORMAT/QG_MARKUP` 等确定性门禁 | 语义准确性和中文自然度 |
| `terminology.tsv` | 术语依赖、适用范围和 preferred 证据 | 整句质量 |
| runtime collision 工具 | `QG_RUNTIME` 和一致性风险 | 某个统一 target 是否语义最佳 |
| review/findings | 结构化问题 observation | 未报告条目一定无问题 |
| remediation ledger | finding 的处置与证据 | 修订后的新 revision 已完成全量复审 |
| manifest/snapshot | 版本和来源可复现性 | 译文当前语义正确 |
| build/smoke | 产物完整性和运行结构 | 全部文本在 UI 中自然、无截断 |

质量系统应复用上述实现，不另造一套 Lua 解析、printf 解析或运行时键语义。

## 十二、治理、安全和发布边界

1. 质量 inventory、sample、review 和 report 默认只写 `.artifacts/i18n/quality/`。
2. 任何模型评价都必须使用有界 bundle，不得让模型读取项目、工具或会话。
3. 首次向外部 provider 发送质量 bundle 时，继续遵守项目 Pi 审核授权流程；质量命令不得隐式联网。
4. 模型 finding 不能直接晋级、降级或修改规范文件，必须经过宿主校验和人工裁决。
5. bundle 和版本控制数据不得包含绝对路径；公开代码证据使用相对路径和固定 commit。
6. 质量工具不得自动安装、发布或改写 addon 仓库。
7. 对外导出的翻译记忆应附带适用游戏版本、生成摘要和项目许可证/上游来源说明。
8. 所有质量 schema、policy、taxonomy 和基准集都要版本化；破坏性变更提升 contract 版本，不原地重解释历史数据。

## 十三、分阶段实施

### 阶段 1：质量清单与校准试点

- 定义 v1 taxonomy、severity、profile、身份和严格 schema；
- 生成全量 revision inventory 和确定性风险特征；
- 生成可复现的 120 条分层试点样本；
- 双重独立评价并人工裁决；
- 形成首份一致性、错误分布和规则可用性报告；
- 不构建面向用户的模糊匹配，不给全语料自动贴 Gold。

详见 [`translation-quality-phase-1.md`](./translation-quality-phase-1.md)。
当前 Evaluator v3/Facts curation 的离线收口实施细节见
[`translation-quality-offline-closure-plan.md`](./translation-quality-offline-closure-plan.md)。

### 阶段 2：精确高质量译文库

- 将经验证的 current revision 质量证据规范化；
- 建立 Gold/Silver 精确 TM 和 variant 条件；
- 加入 revision 变化自动失效和术语依赖检查；
- 提供只读查询和导出，不自动应用。

### 阶段 3：模糊匹配与联想

- 建立结构兼容过滤、词法/语义候选生成和高风险差异检测；
- 在冻结基准查询集上校准 Top-K；
- 展示来源、差异、等级、置信度和适用范围；
- 达到精度门槛后再接入 proposal 工作流。

### 阶段 4：反馈闭环和持续校准

- 记录建议是否采纳、修改量和后续缺陷；
- 建立抽样复核和自动降级；
- 按版本重建索引并保留历史 revision；
- 评估是否需要更细的片段对齐、领域模型或 UI 运行测试。

## 十四、总体完成标准

整体系统达到可用状态至少应满足：

- 任一质量结论都能追溯到 current `revision_id`、规则版本和证据；
- 自动门禁失败不会被总分或模型意见覆盖；
- Gold、Silver、Candidate、Quarantine 的晋级与降级可复现；
- 同一 source 的合法 variants 保留上下文条件，不发生无证据全局合并；
- 模糊检索在冻结查询集上达到预先定义的精度目标；
- 所有建议均显示质量、置信度、适用范围和高风险差异；
- 质量工具只生成 artifact，不自动修改规范 Lua 或发布仓库；
- 游戏版本、译文 revision 或相关术语变化会可靠使旧认证失效。
