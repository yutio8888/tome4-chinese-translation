# 翻译质量工程离线闭环执行方案

> 状态：全部完成（2026-08-08）。工程（2.1–2.4、2.6）、五角色执行
> （§14–15 两轮，v5 契约修订后 Gold 冻结）、以及经多轮授权契约修订后的
> **外部 33-slot campaign 全部 33/33 槽通过**，官方因果报告生成
> （`translation-quality-facts-study-report-v1.md`；工作期归档索引逻辑路径为
> `.artifacts/i18n/quality/facts-study-campaign-archive.json`，长期 A-core 归档身份为
> `ee8973e1…`，本体不进入源码仓库）：
> **do-not-promote-facts-channel**（Luna 判据 3/7 失败；DeepSeek 方向正面
> 但不足以推广；holdout_clearance=false）。详见 `../handoff.md` §14–§16。
>
> 更新时间：2026-08-08。
>
> 上位设计：[`translation-quality-system.md`](./translation-quality-system.md)；
> 当前状态与实验交接：[`../handoff.md`](../handoff.md)。

## 一、目标与停止点

本轮在不调用外部 provider、不运行 v4 holdout 或正式 120 条、不修改规范 Lua
和术语内容的前提下，完成以下离线闭环：

1. 收口当前尚未提交的 Evaluator v3 与 Facts Study 工作；
2. 提取共享 claim、证据和 artifact 核心，同时保持 v1–v3 历史语义不变；
3. 建立版本化数据集登记和完整嵌套 schema；
4. 实现 `facts-study-curation-v1`，生成约 80 条候选池并筛选最终 20 条；
5. 通过隔离子代理完成 Facts、curator、Gold A、Gold B 和 adjudicator 五个角色；
6. 冻结满足配额的 Gold，完成 33-slot 非证据性 fake replay；
7. 停在任何外部授权、provider 调用和 v4 准入之前。

工具生成物继续只写入 `.artifacts/i18n/quality/`。本轮不提交、不推送，
最终交付为通过全部门禁的工作树改动与忽略目录中的可重建 artifact。

## 二、实施顺序

### 2.1 收口与可复现基线

- 保留当前脏工作树，记录开始时的 `git status --short`、`git diff --name-only`
  和 `git diff --stat`，不得清理或覆盖现有 v3/Facts 改动。
- 给 `test_quality_v2.py`、`test_quality_v3.py` 增加与 Facts 测试一致的
  `tools` 路径 bootstrap，使交接文档中的测试命令可在干净 shell 直接运行。
- 当前 v3/Facts 测试转绿后再进入重构；保存相同 fixture 的输出摘要作为兼容基线。
- 最后统一更新 handoff、质量 README 和总体设计状态，中途不反复改写状态文档。

### 2.2 共享 claim 与 artifact 核心

新增两个公共模块：

- `quality_contracts.py`
  - 规范 JSON 字节与 SHA-256；
  - 严格字段、枚举、SHA 和相对路径校验；
  - `ArtifactRef`、subject identity 和结构化 provenance；
  - 公共 JSON 读取逻辑。
- `quality_claims.py`
  - evidence span 规范化；
  - exact `claim_signature`；
  - claim 兼容判断、对称最大权匹配和稳定聚类；
  - 独立的不确定性状态与路由。

统一 claim 规则：

- subject 支持 `canonical-revision` 与 `controlled-mutation`；
- exact identity 绑定 subject、error family、phenomenon、meaning change 和
  source/target evidence；
- 聚类要求同 subject、证据相交、分类兼容且 meaning change 不矛盾；
- `unknown` 可参与匹配但必须进入人工路由，`evidence-invalid` 直接拒绝；
- `other`、`taxonomy-unknown`、`context-insufficient`、`evidence-invalid`
  保持不同状态，均不得自动派生为 minor；
- anchor 使用 exact signature；matcher 使用兼容聚类；stability 同时报告
  exact 与 compatible 指标。

兼容策略：

- v2、v3、旧 Facts 分别使用 `legacy-v2`、`legacy-v3`、`legacy-facts` profile，
  输出保持现有语义；
- 新 curation 和后续 v4 使用 `canonical-v1`；
- 旧模块保留原导出名称，通过 re-export 调用公共实现，不改变历史 contract 或 artifact。

### 2.3 数据集与 schema 治理

新增版本化 `dataset-registry-v1`。每个登记项包含：

- dataset ID、用途、状态和 sample contract；
- sample ID 与 SHA-256；
- 排序后的 revision IDs 与集合摘要；
- 是否排除于后续 calibration、Facts curation 和 holdout；
- natural/controlled 范围与处置说明。

首版登记正式 120、32+32、探索集、失败 pilot、随机候选、长文本候选和舍弃候选。
旧 `facts-study-exclusions-v1` 保持不变，新 loader 使用两者并集。

工具不得自动修改版本控制中的 registry。每次冻结只生成
`registry-fragment.json`，由主代理校验后显式合入。

补齐以下新契约的完整 `$defs`，不再只约束顶层数组：

- claim、evidence、provenance 公共定义；
- curation pool、curator bundle 和 curator assessment；
- Facts author bundle v3 与 Fact packet v3；
- sample v2；
- Gold、Gold review 和 Gold adjudication v2；
- preregistration v2、protocol v3 与 report v2。

Python validator 继续负责跨 artifact、hash、lineage 和配额校验；不新增运行时
JSON Schema 依赖。

结构化 provenance 固定为：

```text
kind: terminology | public-source | versioned-context
resource: repository + revision + logical_path + file_sha256
locator: line-range | term-row | context-key + value
```

禁止在 `logical_path` 中混入 `:line`。

### 2.4 Curation 命令与数据流

新增独立模块 `facts_curation.py`，避免继续扩大 `facts_study.py`，并为
`tools/i18n quality` 增加三个命令。

#### `facts-study-curation-build`

输入为 inventory，固定 seed `tome4-facts-study-curation-v1`，排除集自动来自 registry。

输出：

- 80 条 `curation-pool.json`；
- target-blind `facts-author-bundle.json`；
- Fact packet v3 草稿；
- build report。

候选池固定构成：

| source-side opportunity | 数量 |
|---|---:|
| 术语/专名 | 20 |
| 机制/条件/数字 | 20 |
| 实体关系 | 15 |
| UI role | 15 |
| 一般语义/clean-control 机会 | 10 |

选择只能读取 source、source tag、section、profile、公开上下文和术语特征；
任意替换 target 后结果必须不变。候选按模型可见公共输入去重。非术语条目优先位于
80–1500 字符，术语条目允许更短；无法满足时必须显式报告。

#### `facts-study-curation-prepare`

输入为 pool 与冻结 Fact packet。校验 supplemental-only、英文元语言声明和
provenance 后，输出 target-visible curator bundle 与 curator assessment 模板。

Facts statement 统一使用英文元语言；必要中文规范译名只作为引号内字面值。
语言一致性由作者声明和 curator 人工复核，宿主不使用不可靠的自动语言检测。

#### `facts-study-curation-select`

输入为 pool、Facts、curator assessment，以及可选 controlled mutations。

自然候选按固定 seed 和稳定 ID 选择：

- 8 个 `fact-dependent-defect`；
- 6 个 `surface-defect`；
- 6 个 clean/acceptable，其中至少 5 个 clean、3 个 fact traps。

优先 natural，并在分类内尽量覆盖不同 source opportunity stratum。若自然
fact-dependent 不足：

1. 首次执行返回状态码 2，输出准确 shortfall 和受控变体 bundle；
2. curator 只为缺失数量提供最小受控 target 变体；
3. controlled 只能补 fact-dependent 缺口，最多补至 8 条；
4. 变体不得改变 printf、markup、token 或参数结构，每个 base 最多一个；
5. 若补充后仍不满足配额，返回失败，不得放宽门槛。

controlled identity 使用独立 identity contract，绑定 base revision、变体 target、
mutation kind 和摘要；不得冒充 current canonical revision。`origin` 和 mutation lineage
不进入 evaluator bundle。

成功输出 sample v2、最终 20 条对应的冻结 Fact packet、Gold A/B 与 adjudication 模板、
selection report 和 registry fragment。

### 2.5 隔离角色执行

按以下顺序使用五个无上下文子代理：

1. Facts author；
2. target-visible curator；
3. Gold reviewer A；
4. Gold reviewer B；
5. adjudicator。

Gold A/B 可以并行，其余按依赖串行。执行规则：

- 使用 `fork_turns=none`，任务消息只携带相应有界 bundle；
- Facts author 只读明确列出的 terminology 和 manifest 固定公开源码，禁止读取规范译文、
  target、Gold 和其他 artifact；
- curator 只接收 source、target、冻结 Facts 和 bounded context；
- Gold A/B 只接收最终 sample、Facts 和正式字段说明，互不可见；
- adjudicator 只接收匿名化的两份 review；
- 明确禁止非授权文件/工具访问并审计子代理工具调用；artifact 标记
  `isolation_mode=auditable-soft`，不得声称系统级强隔离；
- 每个角色只输出 JSON，主代理负责保存、严格校验和重算 hash，不补写事实或 claims。

若需要 controlled variant，由原 curator 在收到 shortfall bundle 后单独完成；Gold reviewers
看不到 origin 或 mutation lineage。

### 2.6 Gold 冻结与 fake replay

Gold 冻结必须同时满足：

- 两位不同 reviewer 和独立 adjudicator；
- 至少 8 个 fact-addressed claims；
- 至少 8 个 fact-unaddressed claims；
- 至少 5 个 clean items；
- 至少 3 个 fact traps；
- natural/controlled 指标可分离；
- 所有 claim、evidence、Fact 引用和 provenance 可重算；
- Gold 内容逐字节等于 adjudication 输出。

随后按新 contract dispatch 现有七 arm 逻辑：

- 生成 A/B/C/D/N/L/F bundle；
- 生成固定 33-slot schedule；
- preregistration 状态固定为 `offline-frozen`；
- 新 preregistration 不得被外部 runner 接受；未来外部阶段必须另建绑定用户授权的
  execution manifest。

运行 `facts-study-validate --fake-runner` 和 `facts-study-report`：

- 必须生成并验证完整 33 份 fake assessment/report；
- 报告固定为 `non-evidentiary-offline-replay`；
- natural、controlled 和 pooled 指标分别输出；
- 不产生 Facts promotion、holdout clearance 或任何外部执行权限。

## 三、测试计划

- **公共核心**：canonical hash、路径安全、span、exact signature、兼容匹配、方向无关和稳定 tie-break。
- **兼容回归**：v2、v3、旧 Facts fixture 在重构前后得到相同 ID、cluster 和报告摘要。
- **不确定性**：四种状态分别拒绝或路由，均不静默变成 minor。
- **Schema**：合法完整 artifact 通过；未知字段、浅层非法 item、坏 evidence/provenance 被拒绝。
- **Registry**：重复 ID、摘要不符、保留集重叠、遗漏历史 exclusion 全部失败。
- **Source-side selection**：替换全部 target 后 80 条选择逐字节不变。
- **Curation**：自然配额成功、受控补足、受控仍不足、重复公共输入、结构破坏和隐藏 lineage 泄漏。
- **角色边界**：Facts bundle 不含 target；evaluator bundle 不含 origin、mutation、Gold、历史 finding 或 risk flag。
- **Gold**：角色身份冲突、claim 配额不足、错误 Fact 引用和 adjudication 不一致全部失败。
- **集成**：80 → Facts → curator → 20 → Gold → 七 arm → 33-slot fake replay 全链路。

最终统一运行：

```bash
python3 -B tools/i18n doctor
python3 -B tools/i18n lint --strict
python3 -m unittest -q tests/i18n/test_quality_v2.py tests/i18n/test_quality_v3.py tests/i18n/test_facts_study.py
python3 -m unittest -q tests/i18n/test_toolchain.py
python3 -B tools/scan_runtime_collisions.py
python3 -B tools/classify_runtime_keys.py
git diff --check
```

最后进行一轮全新、只读、无上下文复审。

## 四、验收标准与默认决策

- 本轮停止点为 33-slot fake replay 和干净只读复审通过；
- 不调用 Pi/provider，不申请或沿用任何外部授权；
- 不运行 v4、holdout 或正式 120 条；
- 不修改规范 Lua、`terminology/`、发布仓库或历史 artifact；
- Facts 使用英文元语言；
- controlled 仅在自然 fact-dependent 配额不足时启用，且不能授予后续 clearance；
- 子代理采用可审计软隔离，报告中明确其证据等级；
- 工具只生成 registry fragment，不自动改写权威 registry；
- 不全面拆分现有大型模块，只提取本轮需要的公共 contract/claim 核心；
- 所有文档、schema 和实现的破坏性变化使用新 contract，不重解释 v1–v3；
- 所有项目门禁通过，工作树没有任务范围外的意外改动。
