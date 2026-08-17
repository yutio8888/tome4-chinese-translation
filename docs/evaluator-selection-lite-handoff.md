# Handoff：Evaluator Selection — 收缩为 Selection-Lite v1 的讨论结论

> 类型：讨论/决策记录（working handoff），非规范契约、非门禁、非路线图替代品。
> 记录日期：2026-08-16。
> 本文件本身**不属于** Task A(P0) 或 Task B(SPEC) 的提交范围；它是两项任务的输入依据。
> 若要纳入版本控制，请单独提交，勿混入 P0 或 SPEC commit。

## 0. 一句话结论（BLUF）

采用 **Selection-Lite v1**：以最小可审计契约支持"一次个人项目 evaluator 选型决策"，
而**不**建设完整 evaluator benchmark 平台。原 P0–P5 全量方案(320→160→Dev80/Holdout80、
7 schema、双 preregistration、commitment lifecycle、paired stratified bootstrap、完整
S0–S10)保留为 **deferred escalation specification**，只有触发条件出现才激活。

执行顺序固定：**先 Task A(P0 卫生)，审核通过后再 Task B(Lite SPEC，只写规范不实现)**，
两者分开提交/审阅，不混合。当前只启动 Task A。是否进入 IMPLEMENT 待 SPEC 审完再决定。

## 1. 为什么收缩（判断依据）

1. **与项目自身路线图冲突**：`docs/project-roadmap.md`(2026-08-16)当前主线是 P1 核心
   译文优化；第七节「明确暂缓」点名"为了完善研究设施而新增与当前译文批次无直接产出的
   基础设施"。一个全量 evaluator-selection campaign 正是该条暂缓对象。
2. **服务的下游本身 deferred，价值派生于未启动的下游**：evaluator 选型是 roadmap §5
   启动 P4 正式质量试点四项解除条件之一；P4 整体 deferred，其下游(正式 120、M5/M6、
   Gold/Silver TM)长期/远期。`i18n/quality/README.md` 自承"价值派生于未启动的下游"。
3. **统计严谨度是发表级基准规格，超出个人选型决策所需**：holdout commitment、双
   preregistration、paired stratified bootstrap 防的是 overfitting / researcher
   degrees of freedom / 对外声明可审稿性——这些在"单人选一个 evaluator、随时可推翻"
   的场景下收益极低。
4. **真正的成本闸门是人工**：全量要求 Dev80 + Holdout80 + Challenge24 逐条主判+复核+
   源码核验，是单人 180+ 条多轮标注。工具便宜，人工昂贵。
5. **仓库已有重复模式**：v1/v2/v3 + facts-study v1–v5 + dataset-registry 大量契约最终
   落到 `do-not-promote` / `deferred`。再叠一层全量框架有重演"造契约但到不了 payoff"
   风险。

## 2. Lite vs 全量：范围对照

| 维度 | 全量(原 P0–P5) | Selection-Lite v1（采用） |
|---|---|---|
| 定位文档 | draft → 正式设计基线 | full protocol 标为 deferred escalation spec；另立 lite 规范 |
| contracts | 7 个 schema | 4 个（protocol / sample / assessment / run-manifest） |
| 身份层 | bundle/route/run_config/execution 四层独立 | `bundle_id` / `run_config_id` / `execution_id`；route 为 run_config 字段 |
| preselection frame | cap 320 | 64–96 |
| final pool | 160（Dev80 + Holdout80） | Dev 32 + Primary 32 + Extension 32 |
| Challenge | 独立冻结 view，24 条，正式阶段 | **删除正式阶段**；仅保留 execution-gate fail-fast |
| 候选数 | 6–10 → 3–4 → 2 | 3–4 → 2（预筛后直接进 Dev-32） |
| 统计 | paired stratified bootstrap，S0–S10 | 计数 + 比例 + Wilson/二项区间 + paired 比较 |
| preregistration | sampling + execution 双预注册 | 折入 protocol；只冻结"决策顺序 + holdout 承诺 hash" |
| holdout | commitment 不存 exact IDs | tracked 存 `holdout_commitment_sha256`；exact IDs 落本地 ignored artifact |

## 3. 升级为 Lite 核心原则的四点（不再是备注）

以下四点在讨论中被明确**升级为 Lite 协议一等原则**：

### 3.1 requested configuration 与 observed identity 分别记录
- run-manifest 必须保存**实际观测**的 provider/model/version，与**请求**配置分开记录。
- 消费 assessment 前要求两者一致；不一致直接判 `invalid-execution`（fail-closed）。
- `execution_id` 本身不因 observed identity 复杂化，仍
  `= hash(bundle_id + run_config_id + run_number + dispatch_id)`；observed 值只入
  manifest 供校验。**目的是防路由漂移，不是研究形式主义。**

### 3.2 看到任何候选结果之前冻结决策顺序
- 承认 Dev-32 很可能只能给出"没有明显质量差距"，因此 **operational axes 是生产选型的
  一等指标，不是边缘 tiebreak**。
- 冻结的决策顺序：
  1. correctness / safety gates（schema/execution 成功、完整覆盖、evidence 有效、不乱
     报 presentation-only、不伪造上下文/源码事实）；
  2. decision-changing miss 比较；
  3. false findings / human review burden 比较；
  4. stability 比较；
  5. 最后才 latency / cost。
- 若前面各项差异均低于 practical margin → 正式输出 `practically-indistinguishable`。
- practical margin 与该顺序必须在**结果可见之前**写入 protocol（唯一保留的
  preregistration 纪律；理由：阻止事后为已偏好模型找理由）。

### 3.3 删除正式 Challenge-16 阶段
- 3–4 个候选直接跑 Dev-32。
- 头几个 execution 若出现 schema failure / 明显 hallucination / presentation-only 泛滥
  等**资格性失败**，可 fail-fast 停止该 route——但这是 **execution gate**，不是新的
  dataset / view / 统计阶段。
- 候选恢复到 6+ 时才重新启用 Challenge funnel（列入 escalation）。

### 3.4 progressive evidence 挂在日常 P1 翻译循环上
- 真实批次中"Paseo REVIEWER(`translation_contextual_v1`) → 人工/源码裁决"产生的已裁决
  样本，按预定抽样规则沉淀进 **append-only evidence pool**。
- evaluator selection 的主要长期数据来源 = 汉化工作副产品，而非与汉化争时间的独立研究
  项目。
- 注意：这是 Lite **有意区别于全量协议**之处——`docs/translation-quality-evaluator-
  selection-v1.md`(§18、§末)明确声明"不以未跟踪的 `docs/project-roadmap.md` 为规范
  依据"；Lite 反而刻意与 P1 roadmap 循环耦合，此偏离须在 SPEC 定位段写明。

## 4. 成本闸门原则（必须写入 SPEC）

> Lite 的主要成本不是基础设施开发，而是 Dev-32 的独立人工语义裁决与必要源码核验。
> 只有维护者愿意承担这笔人工成本时，才进入实际 campaign。

推论：P0 / P1-lite(4 contracts) / P2(Paseo purpose) 可以先做好；若当前更值得直接修
译文，则可以不急着做 Dev-32，这是一个自然停止点。

## 5. Lite 数据规模与漏斗（冻结建议值）

```text
Selection candidate frame:   64–96
Selection Dev:               32
  └─ Dev-32 组成建议:
       10–12 clean / acceptable
        8–10 decision-changing defects
         5–6 terminology / entity-role
         其余 context-dependent / ordinary substantive
Hidden confirmation:
  ├─ Primary:                32（先只冻结 ID；可待 Top-2 出来后再人工裁决）
  └─ Extension:              32（一开始冻结 ID；仅 Primary 无法区分时才投入人工）

候选漏斗:
  3–4 candidates → Dev-32(一次) → Top-2 → 第二次 Dev-32(稳定性)
    → Primary-32 → 够区分? → 是: select / 否: Extension-32
  （只有 Top-2 值得重复运行）
```

## 6. Paseo selection purpose（P2）

- 新增并激活 `role=reviewer` / `purpose=evaluator_selection_v1`；沿用
  `translation_contextual_v1` 的轻量编排纪律(workspace / parent lineage / fresh-session
  / 只读守卫 / candidate identity / dispatch_id)，仅 purpose 不同。
- **保留 no direct-provider fallback**（否则结果混合 Paseo 与另一 runner 行为，不可
  解释）。
- 模型最小输出：`revision_id`、`assessment_state`、`context_sufficient`、
  `findings[]{error_family, phenomenon, meaning_change, source_evidence, target_evidence,
  explanation}`。
- 模型**不**决定：severity、Gold/Silver、reuse eligibility、TM eligibility、最终综合
  评分——这些由宿主或人工派生。
- 该任务属基础设施变更，须 REVIEWER 与 SENIOR_REVIEWER 从同一 SPEC/diff 独立交叉审核。

## 7. 指标优先级（务实版）

第一层"能不能用"（correctness/safety gate，见 3.2 第 1 项）先于第二层"模型质量"。
第二层建议新增两项个人项目关键、基准常忽略的指标：
- `false findings per 100 revisions`
- `human review burden per 100 revisions`

示例：A recall 92% / 7 伪 finding 每百条 vs B recall 94% / 34 伪 finding 每百条——维护
数万条译文时 A 很可能更适合作默认 evaluator。

## 8. 全量协议的处置：deferred escalation specification

`docs/translation-quality-evaluator-selection-v1.md` 状态由
`evaluator-selection/1.0-draft` 改为 **`design-reference / full protocol deferred`**，
header 直接内联 activation conditions（英文示例，SPEC/文档中定稿）：

```text
Activation requires at least one of:
- public comparative benchmark publication;
- evaluator output gains automatic Gold/Silver/TM authority;
- Lite cannot distinguish production candidates and the distinction matters operationally;
- multiple independent maintainers/annotators require stronger experiment governance;
- evaluator findings can trigger automatic translation modification without mandatory
  human review.
```

即：它是 escalation specification，不是 backlog。避免后续 agent 把 320→160→bootstrap
当成必须完成的工程要求（复用仓库既有 idiom：README/roadmap 已用"四项解除条件"固定 v3
deferred 状态）。

## 9. 任务边界

### Task A — P0 hygiene（现在启动，先做）
1. 将 `docs/translation-quality-evaluator-selection-v1.md` 状态改为
   `design-reference / full protocol deferred`，并内联 §8 的 activation conditions；
   **不**把它提升为"承诺执行完整 P1–P5 的正式设计基线"。
2. 修正 `i18n/quality/README.md` 第 118–119 行的 stale 表述：现行 `translation_
   contextual_v1` 运行时身份已解耦（近期 commit `79c5d63` decouple runtime identity、
   `5b2f8d0` Muse primary / DeepSeek backup），不再固定 `pi/opencode-go/deepseek-v4-
   flash`。修订须只更新运行时身份表述，**不**改写 prereg-v2 不兼容的历史 deferral 逻辑。
3. 明确工作树中其他用户改动**不属于**本任务（见 §10 分类）；不混交、不顺手 stage。
4. 退出条件：协议文档定位为 deferred escalation；README stale 表述已修；工作树基线分类
   清晰；**不调用 provider**。

### Task B — evaluator-selection-lite-v1 SPEC（Task A 审核通过后）
只写规范，不实现。冻结章节顺序：
```text
定位与 progressive evidence
  → decision policy（含 3.2 冻结决策顺序 + practical margin）
  → requested/observed identity（含 invalid-execution 语义）
  → Dev-32
  → Primary / Extension
  → 四类最小 artifact（protocol / sample / assessment / run-manifest）
  → Paseo boundary（purpose=evaluator_selection_v1，no direct-provider fallback）
  → artificial / real evidence separation（fake replay 标 non-evidentiary）
  → cost gate（§4）
  → escalation conditions（§8）
```
写完后再决定是否值得 IMPLEMENT。

## 10. 工作树现状与必须处置的 OPEN ITEMS（重要）

当前 `git status` 分为三类，Task A 须显式分类、不混交：

**(a) 与本讨论无关的既有用户改动——不属于 Task A/B：**
- `README.md`（M，+2 行）
- `tests/i18n/test_ai_state_check.py`（M，1 行）

**(b) 已存在但需在 Task A 中厘清 provenance 的改动：**
- `i18n/quality/README.md`（M，+4 行）——pending diff 触及第 32 行附近与第 90–91 行附近，
  **并未**触及第 118–119 行 DeepSeek 表述。即 stale 修复尚未做；须先确认这 4 行既有改动
  来源，再叠加 Task A 的 DeepSeek 修订。
- `docs/project-roadmap.md`（??，untracked）——路线图，独立于 selection 工作。

**(c) ⚠️ 已开工的全量实现，早于 Selection-Lite 决策，须单独裁定处置：**
- `tools/i18nlib/quality_selection.py`（**825 行**，untracked）
- `tests/i18n/test_quality_selection.py`（**634 行**，untracked）
- `i18n/quality/selection/protocol-v1.json`（全量 protocol JSON，untracked）
- `i18n/quality/schemas/evaluator-selection-*.schema.json`（**8 个全量 schema**，untracked）

  这批共约 1,459 行实现 + 全量 protocol/schema 是**在收缩为 Lite 之前**写就的全量方案
  产物。本次决策是"不采纳全量、只做 Lite 4 contracts"，因此它们需要一个明确处置决定：
  隔离归档 / 丢弃 / 择部分回收进 Lite。**在该处置决定之前，Task B 的 4 个 Lite
  contract 不应直接覆盖或复用这些文件，以免全量假设悄悄回流。** 这是最高优先的
  open item。

## 11. 当前未授权 / 明确非目标

- 不抽样、不调用任何候选 evaluator / provider。
- 不做人工标注（Dev-32 裁决属未来 campaign，受 §4 成本闸门约束）。
- 不激活 `purpose=evaluator_selection_v1`（属 Task B 之后）。
- 不修改规范 Lua、`terminology/`、发布仓库、历史 v1/v2/v3 artifact。
- 不 push、不同步外部仓库。

## 12. 下一步

现在只启动 **Task A(P0 hygiene)**。这能先消除"完整版是否是待办"的歧义，且不给译文主线
引入新工程承诺。Task A 审核通过后再起 Task B(Lite SPEC)。
