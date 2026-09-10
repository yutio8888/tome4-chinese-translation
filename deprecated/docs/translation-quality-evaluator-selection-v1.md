# 评估器模型选择协议 v1（Evaluator Model Selection Protocol v1）

> 状态：`design-reference / full protocol deferred`，文档变更类（infrastructure）。
> 本文件保留完整协议作为设计参考，是**延期的升级规范**（deferred escalation
> specification），不是当前实现基线，不构成 backlog obligation，也不要求执行完整
> P1–P5 计划。
>
> 激活完整协议要求至少满足以下一项（实际激活仍须另行确定范围、授权、实现与审核）：
>
> - 需要公开发布比较基准；
> - evaluator 输出将自动获得 Gold/Silver/TM 权限；
> - Selection-Lite 无法区分生产候选，且该区分在操作上具有实际意义；
> - 多名独立维护者／标注者需要更强的实验治理；
> - evaluator finding 可以在没有强制人工审核的情况下触发自动修改译文。
>
> 协议版本：`evaluator-selection/1.0-draft`。正文中的维度、统计、生命周期与机器工件
> 设计继续作为完整协议设计参考。任务开始前工作树中的 pre-Lite full implementation
> artifacts 不因本状态而被采纳或激活；其去留已单独裁定为丢弃，身份记录见
> [`evaluator-selection-full-impl-discard-manifest.md`](./evaluator-selection-full-impl-discard-manifest.md)。
> 本文件不调用 provider／候选
> evaluator，不抽样真实 revision，不激活 `evaluator_selection_v1`，也不授予发布或外部传输授权。
>
> 上位规则：[`AGENTS.md`](../../AGENTS.md)；编排契约：
> [`paseo-orchestration-v2-contract.md`](../../docs/paseo-orchestration-v2-contract.md)；活跃译文
> 语境审核契约：[`paseo-translation-context-review-v1-contract.md`](../../docs/paseo-translation-context-review-v1-contract.md)。
>
> 本文档**不修改、不重解释** `translation_contextual_v1` 契约、Paseo 编排契约、
> Evaluator v1/v2/v3 文档、Facts 研究 artifact、`dataset-registry-v1` 或任何历史
> assessment/adjudication/report。

## 一、目的、范围与定位

### 1.1 目的

本协议定义 contract-bound 的 **评估器模型选择阶段（Evaluator Model Selection Phase）**
的可执行、可独立复审、fail-closed 规范：在冻结的候选池、分层样本、人工裁决参考集、
预注册决策语义和隔离墙约束下，从 6–10 条初始候选路由中筛选出至多 2 名 finalist，
并在隐藏封存集上产出最终两两结论（A 优于 B / B 优于 A / 实际不可区分）。

本协议回答的问题只有一个：**在候选评估器路由之间，按预注册端点选择哪一条进入后续
生产评估器配置决策**。它不回答"某条译文是否合格"，也不回答"某条译文能否认证"。

### 1.2 范围

- 范围：设计规范本身。包含全部协议固定值（§5、§6、§8–§13）、预注册边界（§10、§17）、
  阶段机（§13）与隔离墙（§14）。
- 范围外（本文件不实现、不授权、不声称存在）：
  - 任何代码、schema、dataset 抽样实现或工具命令的落地；
  - 任何 provider 调用、候选 evaluator 运行、外部传输授权；
  - 修改规范 Lua、`terminology/`、发布仓库、活跃契约或历史 artifact；
  - 正式 120 条、M5/M6、Gold/Silver/TM 或生产映射（§14 隔离墙）。

### 1.3 定位与阅读对象

本文件面向 ORCHESTRATOR、Paseo REVIEWER／SENIOR_REVIEWER 以及未来实现者，作为独立
复审和实现依据。协议固定值（protocol-frozen）与预注册固定值（preregistration-frozen）
的区分见 §17；两者在 §10、§11 中按各自边界使用。

## 二、术语

| 术语 | 定义 |
|---|---|
| 预选框（preselection frame） | 有界非 dataset 预选框，cap=320 条 revisions（protocol-frozen），由 S0.5 冻结的确定性 source/risk 排序确定遍历顺序；经 S1.5 人工分类后由 S1.8 精确选出最终 160 池；未被选中的 frame 条目丢弃且永不成为 dataset，不登记 registry（§6.2、§13）。 |
| 候选池（candidate pool） | **最终 160** 条 current natural revisions 的冻结集合（final pool），由 S1.8 从 frame（≤320）中按冻结顺序精确选出（§6.2）；被 Dev 与 Holdout 完全划分：80 + 80 = 160。术语 candidate pool 全篇均指该最终 160，不指 frame。 |
| natural current revision | 当前规范译文中的自然条目（非受控变体 controlled variant），身份按 `tome4-translation-revision-v1` 契约绑定（`tu_uid`/`revision_uid`/`revision_id`/`target`/`args_order`/`special`）。 |
| Selection Dev（开发集） | 80 条分层样本（§6），用于 Challenge 资格筛选与首次 Dev 评分；Challenge 是其子集。 |
| Challenge view（挑战视图） | Dev 中固定 24 条的子集视图，**不是独立 dataset**（不登记进 dataset registry）；在任何路由输出前冻结；只用于 Challenge 漏斗筛选，其指标不计入 Dev/Holdout 最终性能报告（见 §6.3）。 |
| Holdout（隐藏封存集） | 80 条 = Primary 40 + Extension 40；在 finalist 及其 Dev 分析冻结前，任何候选路由不得接触。 |
| 候选路由（candidate route） | 请求的评估器执行配置身份（requested route/configuration）：路由名/ID ＋ 请求的 provider/model 身份 ＋ reasoning/temperature/max output ＋ 执行参数；prompt/bundle/terminology/source 内容 hash 归属 bundle identity，不计入 route identity（§12.1）。路由名与模型身份是**预注册值**，实际观测的 provider/model/version 按 §10.1/§12 记录与校验，不在 S2.8 预冻结。 |
| finalist | 由 eligible/Pareto 路由按预声明字典序 tie-break 选出的前 2 名（同时是 stability entrants，获得第二次独立 Dev 执行）。 |
| 人工裁决选择集（human-adjudicated selection set） | Dev 与 Holdout 上经主标注、第二复核、源码核验、裁决与 clean-control 确认后冻结的人工标签集；全部端点的参考真值。**必须使用该术语，不得称为 certification Gold**（§14）。 |
| 选择状态（selection state） | 每条目的标签：`clean` / `defect` / `context-insufficient` / `source-issue`（§7）。 |
| 原子选择 finding | 单问题 finding，含 family／phenomenon／meaning change、source/target 证据 span、decision impact、context sufficiency、source verification 与 adjudication note（§7）。 |
| false finding（unmatched finding） | 未与任何人工裁决 issue 匹配的 finding（§8、§9）。 |
| reveal | 在既定阶段向决策函数开放既定子集的标签或结果（§10、§13）。 |
| 协议固定值 | 由本文件冻结，修改必须走 infrastructure 变更审核（§17）。 |
| 预注册值 | 在任何路由输出前由预注册事件冻结的数值/身份（§17）。 |
| 隔离墙 | selection artifact 与认证/生产/历史 artifact 之间的单向隔离（§14）。 |

## 三、分离原则（DD1）

评估器模型选择必须与以下流程显式分离；**Translator Model Selection（译者模型选择）不
等同于日常译文修订或 `translation_contextual` 语境审核**：

| 维度 | 对象 | 产物 | 输出去向 |
|---|---|---|---|
| **评估器模型选择**（本协议） | 候选评估器路由 | selection result / selection assessment | 只用于"哪条路由进入生产评估器配置决策"，见 §14 隔离墙 |
| **译者模型选择 Translator Model Selection** | 独立范围外实验（译者侧模型对比） | 实验报告（不在本协议内） | 不参与日常译文修订，不参与评估器选择，不授予生产资格 |
| **日常译文与语境审核（daily translation workflow）** | 日常译文修订与语境审核 | `translation_contextual_v1` 语境审核结果 | 小批次译文修订闭环，不参与模型选择 |
| **生产认证（production certification）** | 正式质量分级与复用库 | Gold/Silver/TM 资格、正式 120 条、M5/M6 报告 | 精确 TM／发布准入；selection 产物绝不授予这些资格 |

规则：

1. 选择执行不得改道或占用日常翻译审核路由；`translation_contextual_v1` 保持为活跃译文
   审核的唯一结果契约（§4.4）。Translator Model Selection 作为独立范围外实验单独管理，
   不占用、不重解释日常译文与语境审核流程。
2. 选择结果（即使出现方向性获胜者）不构成生产认证、holdout clearance 或发布准入
   （§14）。
3. 四个维度共享 Paseo 角色机制时按各自 purpose/契约隔离，不共享输入、输出、finding 或裁决（§4）。

## 四、执行路由与禁止路径（DD2）

### 4.1 唯一执行链

所有未来的选择执行（Challenge、Dev、finalist repeat、Primary、Extension）必须走以下
唯一链条，不得旁路：

```text
Paseo 路由 → 版本化 selection result contract → 结构化 selection assessment
```

- **Paseo 路由**：每次执行由当前 ORCHESTRATOR 经 Paseo REVIEWER（`role=reviewer`）
  派发，遵守 workspace、parent lineage、fresh-session、只读守卫、candidate identity
  与 `dispatch_id` 纪律（与 `translation_contextual_v1` 相同的轻量编排约束，但
  purpose 不同）。派发载荷必须带任务／角色 labels；恢复语义遵循
  `paseo-orchestration-v2-contract.md`。
- **版本化 selection result contract**：reviewer 返回必须符合未来冻结的 selection
  result contract（严格 schema、全序覆盖、evidence 字节一致、身份回显、无未声明字段）。
  contract 的 identity/hash 由未来版本化规范资产固定（§15.1、§17）；campaign preregistration
  只能绑定该 identity/hash，不得任意命名 contract 版本。
- **结构化 selection assessment**：ORCHESTRATOR 按本协议 §8–§9 的端点与匹配规则把
  selection result 规范化为结构化 assessment，并写入忽略目录的派生运行（§15）。

### 4.2 禁止路径

必须禁止以下路径，不得复活、不得以任何别名重建：

1. **已退役 blind runner**：旧 `translation_v2` blind runner（legacy 直接模型盲评通道）
   已退役；本协议禁止其任何形式的重启或等价重建。
2. **直接 provider 调用**：任何未经过 §4.1 Paseo 路由、无版本化 selection result
   contract、无冻结预注册的直接 provider 调用一律禁止。现有 `tools/pi-quality-evaluator`
   与 `tools/pi-quality-facts-study` 的直接模式不得用于选择执行。
3. **路由内部载体例外不存在**：本协议删除任何“直接质量工具可作路由内部载体”的例外。
   任何候选评估器的外部执行只允许经 agent-scoped Paseo REVIEWER（`role=reviewer`）完成；
   未来本地工具只允许构建/校验/匹配 artifact（样本组装、hash、schema 校验、确定性匹配、
   指标计算），不得调用 provider/模型。

### 4.3 不修改活跃契约；未来 selection purpose 的激活边界

本文件不修改 `translation_contextual_v1`（`docs/paseo-translation-context-review-v1-contract.md`）
的角色／purpose、输入边界、结果 schema、candidate identity、冻结 envelope 规则或
fresh-session 语义。

- 本协议固定未来的 selection purpose 名称为 **`evaluator_selection_v1`**（协议固定值，见 §17），但**本文件仅完成设计，尚未激活该 purpose**；实现前必须另行修改 `AGENTS.md`、`.ai/roles/*`、Paseo 编排契约与门禁，并经基础设施交叉审核（REVIEWER＋SENIOR_REVIEWER 独立复审）后方可生效。在此之前不得派发或声称已支持 `evaluator_selection_v1`。
- selection result contract 的版本与身份由**未来版本化规范资产**（见 §15.1）固定；campaign preregistration 只能**绑定其 identity/hash**，不得任意命名或自创 contract 版本。
- **envelope-only 精确读取边界（未来 `evaluator_selection_v1` 强制）**：REVIEWER 在一次派发中**只读**当前 dispatch envelope、其明确引用的公开源码片段与结果 schema，**不得浏览** dataset registry、canonical inventory、其他 sample（含其他 dispatch 的 bundle）、受保护 Holdout 路径或既有 assessment/findings；派发前后按 Paseo bounded-read/只读守卫验证，违反即 fail closed（见 §13、§15）。

### 4.4 授权

本协议不构成任何外部传输授权。每次外部传输仍须按 `docs/paseo-orchestration-v2-contract.md` 外发与兼容（§十一），以
role、purpose 与内容范围为边界单独取得用户授权。

## 五、协议固定尺寸（DD3）

以下尺寸全部为**协议固定值**（变更须走 infrastructure 审核）；除注明外，具体数值的
实例化（如种子、路由身份、revision ID）均为预注册值。

| 尺寸 | 固定值 | 说明 |
|---|---|---|
| 预选框（preselection frame） | **cap=320** 条 revisions（protocol-frozen，非 dataset，不登记 registry，不算 selection dataset） | 有界遍历窗口，按 S0.5 冻结的确定性 source/risk 排序确定顺序；S1.5 人工分类可提前停止，人工成本达 cap 即停止（§6.2、§13） |
| 候选池（final pool） | **160** 条 current natural revisions | 全部 natural；**从 frame（≤320）中按冻结顺序精确选出最终 160**（S1.8，见 §6.2）；池被 Dev 与 Holdout 完全划分：80 + 80 = 160 |
| Selection Dev | **80** | 六层配额见 §6.1（20+10+10+8+8+24 = 80）；Challenge ⊆ Dev |
| Challenge view | **24** | Dev 的固定子集视图，非独立 dataset；从已完整裁决的 Dev 中冻结，主层组成 6/3/3/2/2/8=24（含 8 strict-clean，见 §6.3）；任何路由输出前冻结；只用于 Challenge 漏斗筛选，其指标不计入 Dev/Holdout 最终性能报告（见 §6.3、§11.3） |
| Dev clean/acceptable | **24** | 人工确认 clean/acceptable 层（§6.1 第六层），strict-clean 子集在样本冻结时一并固定（≥12，见 §6.4 与 §18）；六主层均由 §6.1 人工 preliminary stratification 确认，不允许 AI label |
| Holdout | **80 = Primary 40 + Extension 40** | 隐藏封存；finalist 及其 Dev 分析冻结前任何候选路由不得接触；每块 10/5/5/4/4/12=40 固定（pooled 20/10/10/8/8/24，§6.4、§17.1） |
| 初始路由 | **6–10** | 范围由协议固定；requested 数量与路由身份为预注册值（实际观测 version 不在 S2.8 预冻结，见 §10.1/§12） |
| Dev survivors | **3–4**（当足够路由合格时） | 全部资格门与 Pareto 过滤后判定：<3 立即停止，无生产候选；3–4 全进 Dev；>4 才按 §11.3 字典序截断到 4（§11）；Challenge 输出只用于筛选，不计入最终性能报告 |
| stability entrants / finalists | **2** | 从 Dev eligible/Pareto survivors 中按 §11 tie-break 选出的 2 名（合格 <2 停止，无 finalist）；只有这 2 名获得第二次独立 Dev 执行；stability 为强制准入门槛（§8.3、§11.3） |
| 执行次数 | Challenge 与首次 Dev 各**一次**/适用路由；仅 finalist 获得**第二次**独立 Dev 执行 | 第二次 Dev 用于 stability 强制门槛（§8.3）；Challenge 执行只用于筛选 |
| 最终两两结论 | **A 优于 B / B 优于 A / 实际不可区分** | 三选一，无其他结果（§10）；Primary 先判，无结论才在 pooled 80 从头重算同一规则，Extension 单独不推断 |

一致性核对：

- Frame/Pool/Sample 三术语不混淆：**frame ≤320（遍历上界）**，**final pool = 160**，**sample = Dev 80 + Holdout 80 = 160**；未被选中的 frame 条目丢弃，不计入任何 dataset。
- Dev 配额：20 + 10 + 10 + 8 + 8 + 24 = 80；Challenge 组成 6+3+3+2+2+8=24 从中固定；
- 池划分：final pool 160 = Dev 80 + Holdout 80；
- Holdout：每块 10/5/5/4/4/12=40，pooled 20/10/10/8/8/24；clean 12/12 平衡（§6.4）；
- Challenge 24 ⊆ Dev 80：因为 final pool = Dev + Holdout 恰好 160，Challenge 无独立空间；它是对
  Dev 的固定视图。Challenge 条目在 survivor 的 Dev 评分中仍按 Dev 全量 80 评分；
  Challenge 执行是独立的资格筛选执行，其指标**只用于漏斗筛选**、**不计入最终性能报告**（见 §6.3、§11.3 与 §18 解释 1）。
- 预选框不登记 registry、不算 selection dataset；如人工分类成本达到 cap 320 即停止（不扩展），见 §6.2。

## 六、抽样与数据集治理（DD4、DD5）

### 6.1 Dev 主层配额（互斥）

Dev 80 条按下列**互斥主层**配额抽样；次级标签（secondary tags）可以跨层重叠
（例如一条机制条目可同时带术语次级标签），主层之间不得重叠。

| 主层 | 配额 | 内容 |
|---|---:|---|
| mechanics condition/number/range | **20** | 机制条件、数值、范围、单位、极性、触发时机 |
| entity-role/relation/reference | **10** | 施法者/目标、主客体、关系、指代 |
| terminology/proper-name/worldbuilding | **10** | 术语、专名、世界观名物 |
| ordinary mistranslation/omission/addition | **8** | 普通误译、漏译、增译 |
| strongly context-dependent | **8** | 强依赖上下文才能判定的条目 |
| human-confirmed clean/acceptable | **24** | 人工确认 clean/acceptable（strict-clean 子集在样本冻结时固定，≥12，与 holdout 12/12 平衡保持可比） |

### 6.2 排除、预选框、候选池与分配（DD5）

**术语（本节专用，不混淆）**：**frame** = 有界预选框（≤320，非 dataset，不登记 registry）；**candidate pool/final pool** = 最终 160 池；**sample** = Dev 80 + Holdout 80。删除任何“先恰好 160 再要求正好配额”的路径。

1. **排除权威 registry 中已有 revision**：排除 `i18n/quality/dataset-registry-v1.json`
   （contract `tome4-quality-dataset-registry-v1`，含正式 120、32+32、探索集、失败
   pilot、候选集等全部登记项）中登记的每个 revision，以及
   `i18n/quality/facts-study-exclusions-v1.json` 排除清单中的每个 revision。
2. **S0.5 冻结 eligible universe 与确定性排序**：按 **S0.5 已冻结的 inventory/registry/exclusion identities、确定性 source/risk 排序与 frame cap 320、人工分层表单与逐层选择 recipe**（排序与选择 recipe+seed 在 **S0.5 sampling preregistration** 预注册并哈希，不得事后称为预注册）；AI target-blind discovery 仅可参与此阶段的 target-blind 风险排序，不产生任何标签、stratum 归属或人工结论。
3. **S1 构建有界 preselection frame（cap 320）**：按 S0.5 已冻结的确定性排序生成**最多 320** 的 frame；frame 不登记 registry、不算 selection dataset。
4. **S1.5 人工分类（有界，route-blind/output-blind、target-visible）**：按冻结顺序遍历 frame，由人工 target-visible/route-output-blind 逐条分类到六主层；**六层总需求为 40/20/20/16/16/48 时可提前停止**（此时已满足最终 160 的两份配额：Dev 20/10/10/8/8/24 + Holdout 20/10/10/8/8/24 的合计）；**如人工分类成本达到 cap 320 即停止**（不扩展 frame）。该步骤不允许 AI label，且不得向候选路由揭示；所用表单/盲法已在 S0.5 预注册。
5. **S1.8 精确选出最终 160 pool**：从 S1.5 已分类的 frame 中，按冻结顺序与固定逐层选择 recipe **精确选出最终 160**（对应 Dev 与 Holdout 的合并需求）；**未被选中的 frame 条目丢弃且永不成为 dataset**。任一层在扫描到 cap 仍不足以填满其在 160 中的配额则 **fail closed**（不跨层借用，不补抽）。
6. **S2 确定性分为 Dev 与 Primary/Extension**：按 **S0.5 已冻结的确定性 allocation recipe** 将最终 160 的各层按冻结顺序确定性分为 **Dev 80（20/10/10/8/8/24）** 与 **Holdout 80（Primary 10/5/5/4/4/12 + Extension 10/5/5/4/4/12）**；各层内分配顺序与 frame/pool 顺序一致，不跨层。
7. **绑定当前 revision 身份并冻结输入**：每个选中条目绑定当前 `revision_id`（身份契约
   `tome4-translation-revision-v1`）并冻结精确 source/target/context 字节（按仓库现有
   canonical JSON + SHA-256 配方）。source、target、`args_order`、`special` 或身份任一
   变化即视为样本失效，必须重新抽样或失败，不得静默改标。
8. **配额不足或重叠一律 fail closed**：任一主层在排除、确认或分配后无法填满配额 → 停止（不得跨层重新平衡）；同一 revision 出现在两个主层或两块样本中 → 失败。不降低配额、不借用其他层。

### 6.3 Challenge 成员与组成（协议固定）

- Challenge 24 条**从已完整裁决的 Dev 80 中冻结**，是样本定义的一部分，**在任何路由输出之前**固定；组成**固定**为主层 **6/3/3/2/2/8 = 24**，对应 mechanics 6、entity-role 3、terminology 3、ordinary 2、context-dependent 2、clean/acceptable 8（其中 **8 条 strict-clean**）。
- **可估计性门槛（协议固定）**：Challenge 冻结时必须满足至少 **8 个 substantive issues**、至少 **4 个 decision-changing issues**（按 §7/§8 adjudicated 标签计）；否则在任何路由输出前停止。
- Challenge **四端点可估计性（凭人工裁决参考分母保证）**：Challenge 满足 8 strict-clean、≥8 substantive、≥4 decision-changing 且 evaluated revisions>0 时，四个单路由点端点（decision-changing recall、substantive recall、clean FP、review burden）均可计算——无 findings 时 recall/FP/burden 记为 0 亦可算。仅当结构门（§11.1 的 schema/coverage/evidence/final-answer/manifest）失败时，相关路由才不可排序；不得以“单路由点端点不可算”临时缺省。此处无需引用 pairwise bootstrap 的有效 replicate，且不得临时回退。
- Challenge 指标**只用于 Challenge 漏斗筛选**，不计入 Dev/Holdout 最终性能报告；措辞“不进入任何分数估计”仅指不计入最终报告，Challenge 的筛选计分仍按 §11 执行。
- Challenge 成员不得在模型结果出现后调整（包括增删、替换或"修复"）。
- Challenge 不登记进 dataset registry（"non-dataset subset"），不改变池的划分。

### 6.4 Holdout 最小覆盖与分块（DD4，协议固定）

Holdout 80 条预冻结与 Dev 可比的最小覆盖，且**按块固定**：

- **Primary 40：10/5/5/4/4/12 = 40**；**Extension 40：10/5/5/4/4/12 = 40**；pooled **20/10/10/8/8/24** 与 Dev 一致（六层均为互斥主层，次级标签可重叠）；
- **24 条 clean/acceptable 总量中 24 条即 strict-clean**，按 **Primary 12 / Extension 12** 严格平衡（即每个 reveal 阶段各有 12 条 strict-clean 作为 clean-item FP 端点的分母）；
- 全部六层与 clean 分配均由 §6.1 人工 preliminary stratification 在 S1.5 确认，不允许 AI label；
- 不声称语料流行率：Holdout 的分层配额是覆盖性约束，不是对全语料缺陷比例的估计
  （§8.4 再次声明）。

### 6.5 样本冻结、人工分层时序与保管

- **S0.5 sampling preregistration（新增，必经）**：在 S1 前冻结并哈希——eligible universe（inventory/registry/exclusion identities）、确定性 source/risk 排序与 frame cap 320、人工分层表单/盲法与逐层选择 recipe、S2 deterministic allocation recipe（含向 Dev 与 Primary/Extension 的分层分配）、六层配额与失败语义（§13、§17）。S1 起已使用的 sampling seed 不得事后称为预注册；frame 不登记 registry、不算 selection dataset。
- **S1.5 人工 classification（必经，有界）**：按冻结顺序遍历 frame（≤320）逐条分类到六主层；六层总需求 40/20/20/16/16/48 全部填满时可提前停止，成本达 cap 320 即停止不扩展；由 **route-blind/output-blind、target-visible** 的人工完成，不允许 AI label，不得向候选路由揭示；结果驱动 S1.8 精确选出最终 160 与 S2 分配（§6.2）。
- **Dev 标签时序与配额闭环**：Dev 80 的完整 `human-adjudicated selection set`（annotation→second review→source verification→adjudication→clean-control）在 **S2.5** 完成并冻结，且在**首个候选路由输出前**；若 S2.5 的 full adjudication 推翻 S1.5 的任一 Dev 主层配额（20/10/10/8/8/24）、24 clean/acceptable、strict-clean（≥12）或 Challenge 可估计条件（6/3/3/2/2/8、8 strict-clean、≥8 substantive、≥4 decision-changing，见 §6.3），则在首输出前 **fail closed，不替换、不重新分配**；全部人工角色始终 route-blind/output-blind。
- **Holdout 时序与 fail-closed**：Holdout 的 preliminary stratification 同在 S1.5 完成以固定配额与 clean 分配；其 **final adjudication 在 S7、且在该 Holdout 任何候选输出/向决策函数揭示前**冻结并保持密封。若 S7 推翻任一固定配额或 Primary/Extension 的 **12/12 strict-clean**，则 **fail closed**：不替换样本、不运行 Primary、不产生结论。
- **Holdout 保密边界（修正）**：版本控制只保存**不可逆 set commitment、总数、六层配额与 contract/hash**，**不保存 exact Holdout revision IDs、可恢复成员映射或 payload**；精确 ID、成员映射、source/target/context payload、stratum/clean 标签、findings/adjudication 全部为**受保护材料**（§15.1、§15.3）。**Dev/Challenge 身份可公开**（Dev revision IDs 与 Challenge 成员可在版本控制中明文保存）。
- Dev 与 Holdout 的**不可逆 commitment 与配额/hash**在预注册事件中逐项固定并哈希；受保护 payload 不进版本控制。
- 样本 ID 变更（任何 revision 增删/替换）即产生新样本，必须重新走预注册；不得复用
  部分旧样本拼装。

## 七、人工裁决选择集（DD6、DD7）

### 7.1 术语与地位

- 参考标签集必须使用术语 **`human-adjudicated selection set`（人工裁决选择集）**；
  **不得称为 certification Gold**。
- 选择数据不是认证数据：不授予 Gold/Silver/TM 资格、不构成 holdout clearance、不是
  生产准入证据（§14）。

### 7.2 时序、独立性与人工分层

1. **六主层归属由人工分类确认**：§6.1 的六个互斥主层与 clean-control 候选由 **route-blind/output-blind、target-visible** 的人工在 S1.5 按冻结顺序遍历 frame（≤320）逐条分类完成有界确认；**不允许 AI label**，该确认是后续 S1.8 选出最终 160 与 S2 分配及 Challenge 组成的依据，且不得向候选路由揭示。
2. **Dev 标签时序**：Dev 80 的完整 `human-adjudicated selection set`（§7.3 五步）在**首个候选模型输出前**冻结；全部人工角色始终 route-blind/output-blind；以人工裁决参考分母为准。
3. **Holdout 时序**：Holdout 的 preliminary stratification 同在 S1.5 完成以固定配额与 12/12 分配；其 final adjudication 在 S7、且在该 Holdout 任何候选输出/向决策函数揭示前冻结并密封；S7 若推翻固定配额或 12/12 则 fail closed（§6.5）。
4. **只有候选池发现 AI 可以 target-blind**：该类 AI 输入限于 source、source tag、section、profile、术语行、公开源码证据与结构风险特征，**不读取 target**；除此之外的任何标注、复核、核验、裁决或分层角色均不得 target-blind。
5. **AI 发现结果不得展示给选择标注者，也不得作为 label**：AI 输出只能影响"哪些 revision 进入候选池"，不能进入人工裁决选择集或分层确认的任何字段；这不是候选模型 finding。

### 7.3 标注工作流（五步）

| 步骤 | 内容 |
|---|---|
| 1. annotation（主标注） | 标注者对每个条目独立给出选择状态与原子 finding（§7.5），不接触任何模型输出 |
| 2. second review（第二复核） | 第二位独立标注者复核同一条目；两方互不可见，记录分歧 |
| 3. source verification（源码核验） | 按固定公开源码 commit 核验机制/术语/UI 事实；记录组件、相对路径、固定 commit 与关键行为 |
| 4. adjudication（裁决） | 独立裁决者解决状态分歧、finding 拆分/合并/歧义与事实冲突，输出裁决记录 |
| 5. clean-control confirmation（clean 对照确认） | 标为 clean 的条目须经双人确认且适用时完成源码核验，才成为 clean control；全部在路由输出前冻结 |

### 7.4 选择状态（DD7）

每个条目恰好有一个选择状态：

```text
clean / defect / context-insufficient / source-issue
```

- `clean`：人工裁决无任何实质问题（presentation/style 类不构成 defect，见 §9.3）；
- `defect`：存在至少一个人工确认的实质 issue；
- `context-insufficient`：现有冻结上下文不足以形成可靠判定（不等同于自动 clean）；
- `source-issue`：原文/源码自身存在歧义或错误，暂不归责于译文。

`context-insufficient` 与 `source-issue` **单独报告**，并从普通 clean/defect 分母中
排除（§8.1、§8.2）。

### 7.5 原子选择 finding（DD7）

每条 finding 必须包含以下字段（供确定性匹配与人工裁决使用）：

```text
family                错误族（number-range / polarity / entity-role / omission /
                      addition / terminology / proper-name / …；可合并组版本化）
phenomenon            现象（细分类别）
meaning_change        omitted / added / weakened / strengthened / reversed /
                      reassigned / made-ambiguous / none / unknown
source_evidence       quote + occurrence（宿主规范化为字符 span）
target_evidence       quote + occurrence（漏译允许空 target quote 且必须带
                      meaning_change=omitted 与预期语义角色说明）
context_sufficient    yes / no / unknown
decision_impact       changes_rule_understanding / can_change_player_action /
                      required_operation_info_missing / recoverable_from_immediate_context
                      各为 yes / no / unknown（三态，不得把证据不足强制转成 no）
source_verification   verified / unverified / conflict / not-applicable
adjudication_note     人工裁决说明（最终确认状态与理由）
```

逻辑一致性校验必须 fail closed：`context_sufficient=no` 时关键 impact facts 不得全部为
确定的 yes/no 而无证据；证据 span 无法在对应文本中定位即校验失败；finding 缺字段、
枚举非法、ID 重复或 revision 缺失即校验失败。

## 八、端点与指标（DD8）

本协议**不使用不透明总分**：禁止综合加权分、禁止单一分数作为决策输入；每个端点独立
计算、独立报告，逐端点给出点估计与 §10 的 bootstrap 区间。

### 8.1 主端点（primary）

| 端点 | 定义 |
|---|---|
| decision-changing defect recall | 匹配到的 decision-changing defect 数 ÷ 人工裁决的 decision-changing defect 总数（evaluated set 内） |
| substantive issue recall | 匹配到的 substantive issue 数 ÷ 人工裁决的 substantive issue 总数（evaluated set 内） |
| clean-item false-positive incidence | 出现 ≥1 条 false finding 的 clean 条目数 ÷ clean 条目数 |

其中：

- **substantive issue** = 人工裁决选择状态为 `defect` 的条目上的确认 issue；
- **decision-changing defect** = substantive issue 且满足任一：
  (a) `decision_impact.changes_rule_understanding=yes AND can_change_player_action=yes`；
  (b) `decision_impact.required_operation_info_missing=yes`；
- 分母只含 `clean`/`defect` 状态条目；`context-insufficient` 与 `source-issue` 条目排除
  （§7.4）。

### 8.2 操作主端点（operational primary）

```text
review_burden = unmatched false findings / evaluated revisions
false_findings_per_100_revisions = 100 × review_burden
```

- **unmatched false findings** = 未与任何人工裁决 issue 匹配的 finding：
  (a) clean/defect 条目上未匹配的 substantive finding；(b) 一切 presentation/style
  finding（§9.3，禁止且一律计为 false finding + scope violation）。`context-insufficient`
  或 `source-issue` 条目上的非 presentation/style finding 不计入 false findings，单独
  进入 context-insufficient 行为端点（§8.3）。
- **evaluated revisions** = evaluated set 中 `clean`/`defect` 状态条目的数量
  （`context-insufficient`/`source-issue` 排除，与 §7.4 一致）。
- **必须声明**：在该分层集上测得的 burden 不是语料流行率估计，也不代表预期生产
  审核量；它只描述"在该冻结分层集上，该路由每评估一条可判定条目产生的误报
  工作量"。

### 8.3 次级与操作端点（secondary / operational）

次级：

- precision（匹配 finding ÷ 全部 finding）、F1；
- stratum recall（按 §6.1 六层分别报告 recall）；
- evidence validity（证据 span 有效且可定位的 finding 比例）；
- context-insufficient 行为：路由对 `context-insufficient`/`source-issue` 条目的标记
  与人工标记的一致率、此类条目上 finding 的数量与去向（单独报告）。

操作：

- schema success（严格 schema 校验通过率）；
- full-coverage success（冻结顺序全量覆盖通过率）；
- final-answer success（无缺失 final answer 的通过率）；
- stability（finalist 两次独立 Dev 执行的一致性：finding Jaccard、状态/事实一致率）；
- latency、cost（按 attempt 累计）。

stability 为**强制生产准入门槛（mandatory production-admission gate）**：具体阈值在**首个候选输出前**预注册（见 §11.3、§17），两次 Dev 执行后任一 finalist 未过则**停止、无 Holdout 运行、不递补第三名、不放宽阈值**；两次执行均须满足 §11.1 的 schema/coverage/final-answer 有效性。阈值数值仍为 preregistration-frozen，门槛本身为 protocol-frozen。

### 8.4 非流行率声明

本协议在任何报告中都必须显式声明：分层集上的缺陷密度、recall、FP 与 burden **均不
代表语料流行率**，也不代表生产环境的预期缺陷率或审核量；这些指标只适用于被冻结的
分层样本本身。

## 九、问题匹配与裁决（DD9）

### 9.1 确定性匹配

路由 finding 与人工裁决 issue 之间的匹配必须确定性执行：

1. 同一条目（revision_id 相同）；
2. source span 相交、相邻，或都指向同一已知参数/术语；
3. family/phenomenon 兼容（可合并组版本化，如 number↔number-range、omission↔condition、
   terminology↔proper-name）；
4. meaning change 不互相矛盾；
5. target span 若双方均非空，相交、相邻或指向同一目标语义单元。

不得仅依据标题/正文文本相似度匹配。匹配算法版本化、可单元测试、方向对称。

### 9.2 歧义/拆分/合并的人工裁决

`ambiguous`、`split-merge`（一对多/多对一）与无法确定唯一匹配的 finding 必须进入
人工裁决（route-blind，匿名展示 source/target/上下文与规范化 span）。裁决后按最终
映射计算 recall/FP；裁决记录绑定匹配版本与理由。`context-insufficient`/`source-issue`
条目上的 finding 不参与匹配，进入 §8.3 端点。

### 9.3 false finding 与禁止项

- 未匹配的 substantive finding 一律计为 false finding。
- presentation/style finding **禁止**：任何路由执行不得输出 presentation/style finding；
  若输出，一律计为 false finding 并在 run manifest 中记为 scope violation（§11.1
  manifest 完整性门）。
- 不得以"风格偏好/润色建议"替代实质 finding；核心含义未变化的条目，模型 findings
  必须为空。

## 十、预注册决策语义（DD10）

### 10.1 预注册事件与时序（S0.5 sampling / S2.8 execution）

- **S0.5 sampling preregistration freeze**：在 **S1 前**冻结并哈希——eligible universe（inventory/registry/exclusion identities）、确定性 source/risk 排序与 frame cap 320、人工分层表单/盲法与逐层选择 recipe、S2 deterministic allocation recipe（含向 Dev 与 Primary/Extension 的分层分配）、六层配额与失败语义（§6.2、§13、§17）；已在 S1/S2 使用的 sampling seed 不得事后称为预注册；frame 不登记 registry、不算 selection dataset.
- **S2.8 execution preregistration freeze**：在 **S2.5（Dev 80 全量裁决与 Challenge 24 冻结）之后、S3 首个候选路由输出之前**冻结并哈希——已产生的 sample/commitment、requested route/configuration（路由名/请求 provider/model/推理参数等）、预期解析规则、允许的 identity 缺失策略与 mismatch fail-closed policy、prompt/bundle/contract identities、bootstrap seed、stability threshold 与全部运行/决策配置（含 screening 语义与最终决策语义，见 §13、§17）；不冻结尚未观察的 actual model version（实际观测的 provider/model/version 按 §12 manifest 记录与校验，超出允许解析范围则 fail closed，immutable version 不可得时按 §12.3 限制结论）；S0 仅冻结 protocol，不冻结精确 preregistration.
- 预注册必须同时冻结：
  1. **screening 语义**：§11 的全部资格门、漏斗停止规则与 finalist 选择规则；
  2. **最终决策语义**：本节全部优势界、非劣界、bootstrap 配方与 reveal 语义；均为 selection decision rules，不声称多重比较校正。
- 任一预注册冻结后不得因看到结果而修改已冻结语义；S2.8 前不得产生任何候选输出。

### 10.2 配对条目 bootstrap 决策统计

> 本节为 **selection decision rules**，不声称多重比较校正或认证统计结论。每个端点独立按 95% interval 判定，不做多重校正。

- 方法：**冻结主层内的 paired stratified item bootstrap**（在 §6.1 六个冻结主层内分层重抽样；两条 finalist 在同一条目上配对比较，保持 stratum 配额与配对结构；seed 固定且预注册、**2000 次 replicate**）；
- 分母为 0 的处理（协议固定）：若某端点在**原始样本**上分母为 0（例如该端点在 evaluated set 内无分母条目，以**人工裁决参考分母**计），则该端点**不可用于优势判定**，其对比不计为获胜端点；该端点仍报告为不可估计。
- 分母为 0 的处理（bootstrap replicate）：某次 replicate 中某端点分母为 0 时，该次 replicate 对该端点的差值记为 **undefined 并排除**；统计该端点的有效 replicate 数，若**有效 replicate < 95%（<1900/2000）**，则该端点**不可用于优势判定**。
- **non-inferiority 的区间要求（协议固定）**：全部 non-inferiority guards（§10.4）**不只看点估计**，还要求对应端点的**单侧 95% bootstrap bound（名义 .05）**支持预设非劣界（例如 recall 差值的下界 > −5pp、FP 差值的上界 < +5pp、burden 差值的上界 < +0.05）；端点不可估计（原始分母 0 或有效 replicate <95%）则该方向失败。
- 报告：点估计 ＋ 各端点的 95% percentile interval（有效 replicate 的 2.5%/97.5%）以及单侧 bound；分母为 0 的 replicate 排除后不插值、不回填；区间仅作为本 selection 决策规则的组成部分，不声称多重比较校正。

### 10.3 实际优势界（practical-superiority margins，协议固定）

| 对比（候选获胜方向） | 优势界 |
|---|---|
| decision-changing recall 更高 | **+10 个百分点** |
| substantive recall 更高 | **+10 个百分点** |
| clean-item FP 发生率更低 | **低 8 个百分点** |
| review burden 更低 | **少 0.10 false findings/revision（即每 100 条少 10 条）** |

### 10.4 非劣界（non-inferiority guards，协议固定）

候选获胜者相对另一 finalist 必须满足全部：

- 任一 recall 端点不差超过 **5 个百分点**；
- clean FP 不差超过 **5 个百分点**；
- review burden 不差超过 **0.05 false findings/revision**。

### 10.5 方向性获胜规则（selection decision rules）

> 本节为 **selection decision rules**，不声称多重比较校正或认证统计结论；每个端点独立用 95% interval 判定，不做多重校正。

候选 A 相对 B 在**当前 look**（Primary 或 pooled）成为方向性获胜者，当且仅当全部成立：

1. **当前 look 的两 finalist 的当前 scored execution 均通过全部资格门（§11.1 五门：schema、ordered coverage、evidence、final answer、manifest）**；Primary look 为 S8 两 finalist 的 execution 均通过，pooled look 为 S8 与 S9 两 finalist 的四次 execution 均通过（含 S9 时 S9 也须五门齐备），任一 invalid 则该 look 无结论（§11.2）；
2. A 满足全部非劣界（§10.4），且以**单侧 95% bootstrap bound（名义 .05）**验证非劣界（§10.2），任一非劣端点不可估计时该方向直接失败；
3. A 在四个 superiority 端点（§10.3）中**至少一个**同时满足：(a) 点估计达到 practical margin，(b) 原始样本与有效 bootstrap 上可估计（原始人工裁决参考分母不为 0 且有效 replicate ≥95%），(c) 该端点的 **95% paired stratified item bootstrap interval（有效 replicate 的 95% percentile）在方向上排除 0**（paired stratified bootstrap，基于有效 replicate）；
4. 仅比较本 look 的四端点，不跨 look 复用 Primary 区间；

否则该方向不成立。B 相对 A 对称应用。两方向都不成立 → 结果为**实际不可区分**
（practically indistinguishable）。两向都成立在数学上不可能（95% 区间排除 0 的方向唯一）；若出现数据异常，以 fail-closed 处理为实际不可区分并记录。

### 10.6 reveal 语义（Primary → pooled）

1. 先只在 **Primary 40** 上应用完整规则（§10.5 的 95% interval 与 non-inferiority 单侧 bound）；
2. Primary 得出方向性获胜者 → 定论；Extension **不执行**；
3. Primary 无结论（实际不可区分）→ 执行**预冻结**的 Extension（其成员与身份在
   协议/样本冻结时已固定，只是未执行）→ 在 **pooled 80 上从头重算同一规则（§10.5）**（不复用 Primary 的区间结果）→ 定论；
4. **Extension 单独不得产生任何结论**：任何结论只可能来自 Primary 或 Primary+Extension
   的 pooled 结果；不得用 Extension 单独推断。

reveal 顺序在预注册中固定；不得因结果好坏提前/延后揭示。

## 十一、资格、漏斗与 finalist 选择（DD11）

### 11.1 资格门（最低要求，不得静默放宽；适用于每一次 scored execution）

**适用于每一次 scored execution：Challenge、Dev first、finalist repeat（S6）、Primary（S8）、Extension（S9）均必须满足全部五门**，缺一不可：

1. **严格 schema**：selection result 通过版本化 contract schema（无未知字段、枚举合法、
   身份回显一致）；
2. **精确全序覆盖**：按冻结顺序覆盖全部 revision，不重不漏；
3. **evidence validity**：source/target 证据 span 有效且可在冻结文本中定位；
4. **无缺失 final answer**：不缺少最终答案（禁止只有 reasoning 没有 final answer）；
5. **完整 run manifest**：§12 全部字段齐备（含 attempts、failure class 与操作指标）。

附加门槛可以在预注册中增加，但**不得放松**以上最低项。

### 11.2 失败与重试语义

- **content/schema/evidence/coverage/manifest 任一 invalid 不替换**：任一 finalist 的 **repeat（S6）、Primary（S8）、Extension（S9）** 中出现 content、schema、evidence、ordered coverage 或 manifest 任一 invalid（§11.1 五门），则 **不替换、立即停止、无 A/B 结论**，失败执行及其原始输出保留并计入指标；Challenge/Dev 的 invalid 同样不替换，按 §11.3 漏斗停止规则处理。
- **仅 infrastructure error 可 one-retry**：只有 **Paseo infrastructure 错误**遵循活跃 one-retry 规则（`paseo-orchestration-v2-contract.md`）；每次 attempt 都记录；**retry 不能抹掉操作失败指标**（schema success、coverage、latency、cost 按 attempt 累计报告，成功 attempt 与失败 attempt 分开统计）；非 infrastructure 的 invalid 不得重试。

### 11.3 漏斗与停止（含 Challenge 可估计性与 stability 门槛）

```text
初始路由 6–10 → Challenge 筛选（收缩到 3–4） → Dev 首次执行（80 条） → Dev survivors（最多 4） → finalist ×2（stability 强制门槛）
```

- **Challenge 阶段（6–10 → 3–4；指标只用于筛选，不计入最终性能报告）**：
  1. 对 6–10 条初始路由各执行一次 Challenge（24 条）；先应用 §11.1 最低资格门过滤；
  2. 再检查**可排序性（§6.3）**：Challenge 已凭人工裁决参考分母保证 8 strict-clean/≥8 substantive/≥4 decision-changing 且 evaluated revisions>0，四单路由点端点均可算（无 findings 时记 0）；仅结构门（schema/coverage/evidence/final-answer/manifest）失败的路由不具备排序资格，不得临时缺省；仅剩余可排序路由参与 Pareto；
  3. 对剩余可排序路由做 Pareto 过滤（同四端点，被其他 eligible 路由在全部四维度支配者剔除），得到最终前沿；
  4. **最终前沿 <3 → 立即停止**，无生产候选；**最终前沿 3–4 → 全部进入 Dev**；最终前沿 >4 → 按 §11.3 字典序截断到 4 名进入 Dev。
- **Dev 阶段（Dev survivors 最多 4；<2 停止）**：
  1. 对 Challenge survivors 各执行一次 Dev（80 条）；
  2. 应用 §11.1 资格门与 Pareto 过滤（同四端点）得到 eligible/Pareto 集合（最终前沿）；
  3. 最终前沿 <2 → 停止，无生产候选；最终前沿 2–4 → 全部为 survivors；最终前沿 >4 → 按字典序取前 4 为 survivors。
- 不得为继续而降低任一阈值；
- **Pareto 过滤**：被其他 eligible 路由在所有四个维度（decision-changing recall、
  substantive recall、clean FP、review burden）上支配的路由不作为 survivors；过滤**在最终前沿清点前**完成。
- **finalist**：从 Dev 的 eligible/Pareto survivors（最终前沿）中按预声明字典序 tie-break 取前 2（<2 已停止）：

```text
1. decision-changing recall（降序）
2. clean FP（升序）
3. review burden（升序）
4. substantive recall（降序）
5. route ID（升序）
```

- 只有 finalist 获得第二次独立 Dev 执行（stability 强制门槛，§8.3）；非 finalist 的 survivor
  不再运行。
- **stability 强制门槛**：两名 finalist 的第二次独立 Dev 执行后，按**预注册阈值**判定 stability（§8.3）；**任一未过则立即停止，无 Holdout 运行，不递补第三名，不放宽阈值**；两次执行均须满足 **§11.1 全部五门（schema、ordered coverage、evidence validity、final answer、manifest）**，任一门 invalid 即视为未过（与 S6 一致）。

## 十二、运行身份与 manifest（DD12）

### 12.1 四类身份分离

- **bundle identity**：冻结内容 bundle 的身份（source/target/context、术语子集、源码证据与结构化输入的 bytes/hash）；
- **route identity**：**requested** 候选路由执行配置的身份（路由名/ID、**请求** provider/model 身份、reasoning/temperature/max output、跨运行不变的执行参数与预期解析规则；实际观测的 provider/model/version 不属此身份，按 §12.2/§12.3 记录并以 S2.8 允许策略校验）；**不包含** prompt/bundle/terminology/source 内容 hash（归 bundle identity），**不包含** dispatch/attempt/timestamps/实际观测 version；
- **run_config identity**：单次 run 的配置快照（**route identity ＋ bundle/prompt/terminology/source hash ＋ run number**；不含 dispatch/attempt/timestamps）；
- **execution identity**：单次 attempt 的执行实例身份（含 **dispatch/attempt、timestamps、latency/cost、failure class**），与 run_config 分离。
- 内容身份按仓库 canonical JSON + SHA-256 配方计算，与 `translation_contextual_v1`
  的 envelope 纪律同构但独立（selection contract 定义自己的七/多组件 payload，
  不复用 contextual 的 identity 配方）；bundle identity 排除运行时，route identity 不捆绑内容 hash。

### 12.2 selection run manifest

每次计分执行（每个 attempt）必须有独立 manifest，记录至少：

```text
provider                      实际可观测值
route/model                   路由名与模型身份（实际可观测值）
model version                 如暴露则记录；不可得时按 12.3
reasoning / temperature / max output
prompt hash / bundle hash / terminology hash / source hash  # 归 run_config
run number                    # 归 run_config
route identity                # 跨运行不变部分（§12.1）
run_config identity           # route + bundle/hash + run number
execution identity            # dispatch/attempt/timestamps/failure（§12.1）
dispatch / attempt / timestamps
latency / cost
attempts（含失败 attempt）与 failure class（content | schema | infrastructure | timeout | …）
```

观测值超出 S2.8 预注册的允许解析范围则 **fail closed**（见 §10.1、§12.3）。manifest 完整性是资格门之一（§11.1，五门之一）。manifest 与内容身份分开存放：内容身份在冻结
envelope 中，manifest 在派生运行目录中（§15）；route/run_config/execution 三类身份字段不得互换或合并。

### 12.3 版本策略与结论边界（与 S2.8 预注册一致）

- **S2.8 仅冻结 requested route/configuration、预期解析规则、允许的 identity 缺失策略与 mismatch fail-closed policy**，不冻结尚未观察的 actual model version。
- 每次 manifest 记录 **actual observed provider/model/version**（§12.2）；实际观测值超出 S2.8 允许解析范围或与 requested 不一致超出允许策略时 **fail closed**。
- 若 immutable model version 不可用，则所有结论**只适用于被观测的
  route/time/configuration**，不得外推至同一模型的其他版本、其他时间或未观测配置；
  该限制必须写入 selection assessment 与最终报告。

## 十三、阶段机（DD13）

以下阶段机全部 fail-closed：任一阶段的配额不足、overlap、schema 失败或门失败都使
流程停止于该阶段，不产生生产候选，也不得降低阈值回退。

| 阶段 | 内容 | 输出/约束 |
|---|---|---|
| S0 protocol freeze | 本文件（协议固定值） | 仅冻结 protocol（含配额/组成等协议值，不含实例化 preregistration 值；见 §10.1、§13） |
| S0.5 sampling preregistration freeze | 冻结全部抽样相关预注册（eligible universe/排序/frame cap/表单/recipe） | 在 S1 前冻结并哈希：eligible universe（inventory/registry/exclusion identities）、确定性 source/risk 排序与 frame cap 320、人工分层表单/盲法与逐层选择 recipe、S2 deterministic allocation recipe（含向 Dev 与 Primary/Extension 的分层分配）、六层配额与失败语义；已在 S1/S2 使用的 sampling seed 不得事后称为预注册；frame 不登记 registry、不算 dataset（§6.2、§10.1、§17） |
| S1 preselection frame | 有界非 dataset 预选框 cap 320 | 按 S0.5 已冻结的确定性 source/risk 排序生成最多 320 的 frame；不足或重叠即停；frame 不登记 registry、不算 selection dataset（§6.2） |
| S1.5 human classification | 有界人工分类（route-blind/output-blind、target-visible） | 按冻结顺序遍历 frame 逐条分类到六主层；六层总需求 40/20/20/16/16/48 全部填满时可提前停止；成本达 cap 320 即停止不扩展；AI 仅 target-blind 风险排序不标注；结果驱动 S1.8/S2（§6.2、§6.5、§7.2） |
| S1.8 final pool selection | 从 frame 按冻结顺序精确选出最终 160 pool | 按 S0.5 已冻结的逐层选择 recipe 各层按冻结顺序选出最终 160（对应 80+80 合计）；未选 frame 条目丢弃且永不成为 dataset；任一层在扫描到 cap 仍不足则 fail closed，不跨层借用（§6.2） |
| S2 allocation to Dev/Holdout | Dev 80 + Holdout 80（从最终 160 按层分配） | 按 S0.5 已冻结的确定性 allocation recipe 将最终 160 的各层按冻结顺序分为 Dev 80（20/10/10/8/8/24）与 Holdout 80（Primary 10/5/5/4/4/12 + Extension 10/5/5/4/4/12），不跨层；Holdout 仅 commitment/总数/配额与 hash 进版本控制，精确 ID/mapping/payload 受保护；Dev/Challenge 精确 IDs 可公开（§6、§15） |
| S2.5 Dev adjudication + Challenge freeze | 完成 Dev 80 全量人工裁决并冻结 Challenge 24 | 在任何候选输出前完成 Dev 五步裁决与 Challenge 组成（固定 6/3/3/2/2/8 含 8 strict-clean，≥8 substantive 且 ≥4 decision-changing，见 §6.3）；若推翻 S1.5 的任一 Dev 主层配额/24 clean/strict-clean/Challenge 可估计条件则在首输出前 fail closed，不替换、不重新分配（§6.5）；否则 Challenge 从已裁决 Dev 中固定 |
| S2.8 execution preregistration freeze | 冻结执行相关预注册（仅已产样本后） | 在 S2.5 后、S3 前冻结并哈希：已产生的 Dev/Challenge 精确 IDs 与 Holdout commitment、**requested route/configuration、预期解析规则、允许的 identity 缺失策略与 mismatch fail-closed policy**、prompt/bundle/contract identities、bootstrap seed、stability threshold 与全部运行/决策配置（含 §10 的 screening/决策语义与 bootstrap 规则）；**不冻结尚未观察的 actual model version（按 §12 manifest 记录并校验，超出允许范围则 fail closed，immutable 缺失按 §12.3）**；不含已在 S0.5 冻结的 pool/allocation seed；哈希后才允许 S3 首个候选输出（§10.1、§17） |
| S3 Challenge screening | 6–10 条初始路由各执行一次（24 条） | 仅在 S2.8 后执行；按 §11.1 资格门筛选及 §6.3 结构门可排序检查；全部资格门与 Pareto 过滤后清点最终前沿：<3 立即停止，3–4 全进 Dev，>4 字典序截断到 4；指标只用于筛选，不计入最终性能报告 |
| S4 Dev first execution | Challenge survivors 各执行一次（80 条） | Dev 标签已在 S2.5 冻结；**任一五门（§11.1）invalid 按 §11.2 不替换**；attempt 全记录 |
| S5 Dev survivors + finalist | Dev eligible/Pareto 最终前沿最多 4；tie-break 取 2 | 最终前沿 <2 → 停止，无 finalist；最终前沿 ≥2 时 tie-break 取 2 并冻结（§11.3）；不递补 |
| S6 finalist repeat + stability gate | 2 名 finalist 各执行第二次独立 Dev（均为 scored execution） | 每次执行须通过 §11.1 全部五门（schema、ordered coverage、evidence、final answer、manifest），任一 invalid 则按 §11.2 不替换、立即停止、无 A/B 结论；均通过后按 S2.8 预注册阈值判定 stability，任一未过→停止、无 Holdout、不递补（§8.3、§11.3）；通过后 Dev 分析冻结 |
| S7 human holdout adjudication | 主标注→第二复核→源码核验→裁决→clean 确认 | Holdout preliminary 已在 S1.5 完成；final 标签在该 Holdout 任何候选输出/揭示前冻结并密封；若推翻 S1.5 的固定配额或 12/12 则 fail closed，不替换、不运行 Primary（§6.5） |
| S8 Primary（pooled 锁前） | finalist 各执行 Primary 40（envelope-only，scored execution） | 每次执行须通过 §11.1 全部五门，任一 invalid 按 §11.2 不替换、立即停止、无 A/B 结论；REVIEWER 通过当前 envelope 可见当块 source/target/context；路由输出先密封，决策函数再揭示对应 labels 并应用 §10 Primary 规则（95% interval）；有结论则停；除当块 envelope 外不得读 master asset/labels/其他条目或块（§13、§15.3） |
| S9 optional Extension（仅 Primary 无结论） | finalist 各执行 Extension 40（envelope-only，scored execution） | 每次执行须通过 §11.1 全部五门，任一 invalid 按 §11.2 不替换、立即停止、无 A/B 结论；在 80 上从头重算同一 §10 规则；Extension 单独不推断；未执行或 invalid 的 Extension 不得推断 |
| S10 production decision | A 优于 B / B 优于 A / 实际不可区分；或停止无候选 | 输出 selection assessment 与报告；stability 未过或 S7 推翻则无此阶段 |

**Holdout 密封、payload 可见性与读取边界**：

- S1.5 的 preliminary stratification 驱动配额但不揭示受保护 payload；S7 的 final 标签产生并冻结后保持密封，S8/S9 才按块向决策函数揭示对应 labels；候选 REVIEWER 全程不直接读 labels。
- **任何候选路由在 finalist（S5）与 S6 的 stability gate 通过之前不得接触 Holdout**；S6 前任何 Holdout 块的 candidate 输出均禁止。
- **受保护 master asset**（exact Holdout IDs/mapping/full payload/labels/findings/adjudication）仅由 ORCHESTRATOR 的冻结 dispatch builder 与决策函数按阶段读取；
- **候选 REVIEWER 的 Holdout 可见性**：S8/S9 的 REVIEWER **必须**通过当前 envelope 看到当块的 source/target/context（否则无法执行评估），但**除当前 envelope 及其引用的公开源码/schema 外，不得读 master asset、labels、其他条目/块、registry 或 inventory**；路由输出先密封，再由决策函数揭示对应 labels 进行计分。
- 标注者全程 **route-blind/output-blind、target-visible**（§6.5、§7.2），不接触路由输出、候选身份或既有 finding；
- 未来 `evaluator_selection_v1` 的 REVIEWER 读取**仅限 envelope-only**：只读当前 dispatch envelope、其明确引用的公开源码片段与结果 schema，不得浏览 registry/canonical inventory/其他 sample/受保护路径；派发前后按 Paseo bounded-read/只读守卫验证（§4.3、§15）。

## 十四、隔离墙（DD14）

选择阶段的一切产物（pool、样本、challenge/dev/holdout 运行、assessment、报告、manifest、
标签）服从以下单向隔离，**无论选择结果如何**：

1. **不授予认证资格**：不授予 Gold/Silver/TM 资格、不授予 holdout clearance；
   不得把 selection 标签当作认证标签（术语见 §7.1）。
2. **不修改 anchors**：`i18n/quality/anchors-v1.json`、`anchors-v2.json` 及其版本化
   anchor 语义保持不变；selection 不得写入、替换或重解释任何 anchor。
3. **不重解释历史 artifact**：Evaluator v1/v2/v3、Facts 研究（含
   `do-not-promote-facts-channel` 结论与 33-slot campaign artifact）、
   `stability-preregistration-*`、历史 assessment/adjudication/report 全部保持原样；
   selection 不改变其 contract、身份或结论。
4. **不授权 official-120 / M5 / M6**：正式 120 条、M5 人工裁决、M6 报告保持 `i18n/quality/README.md` 与质量系统文档所载的 deferred 状态；selection 不构成其解除条件（本协议不以未跟踪的 `docs/project-roadmap.md` 作为规范依据）。
5. **生产映射与新预注册是独立未来工作**：模型选择完成后，生产评估器配置映射
   （selection result → 生产评估器配置）与新的 preregistration 必须另行设计、另行授权，
   不能由本协议或选择结果自动派生。

## 十五、实现工件与命令边界（DD15）

以下均为**设计级标识**：本文件**不声称**下列任何文件、目录或命令已存在；实现前必须
独立走基础设施审核。

### 15.1 版本控制规范性资产（建议位置，未来实现）

```text
i18n/quality/selection/
  protocol-v1.json               机器可读选择协议（本文件语义的机器表达）
  selection-result-v1.schema.json 版本化 selection result contract schema
  preregistration-v1.json        预注册记录（种子、路由身份、bundle/prompt hash、commitment 与配额，绑定 §4.3 的 contract identity/hash；Holdout 仅含不可逆 commitment/总数/配额与 hash）
  sample-v1.json                 Dev/Holdout/Challenge 样本定义（Dev/Challenge 精确 revision IDs 可明文；Holdout 仅保存不可逆 commitment/总数/配额与 hash，不含 exact IDs/mapping/payload）
  selection-registry-v1.json / registry-v2-fragments/  未来实现必须新建的 versioned selection registry contract 或 dataset registry v2 增量片段（由 ORCHESTRATOR 写入；仅含不可逆 commitment/总数/配额与 hash，不含 Holdout exact IDs、可恢复成员映射、payload、stratum/clean 标签、findings/adjudication；不得把 commitment-only fragment 合入现有 dataset-registry-v1.json，也不得原地改 v1——v1 保持不变，见 §14）
```

> Holdout 边界（重申 §6.5）：版本控制只保存不可逆 set commitment、总数、六层配额与 contract/hash，不保存 exact Holdout revision IDs、可恢复成员映射、payload、stratum/clean 标签或 findings/adjudication；后者全部为受保护材料（§15.3）。Dev/Challenge 身份可公开。现有 `dataset-registry-v1.json` 强制 exact revision_ids，**不能**表达 commitment-only Holdout；未来必须使用新建的 selection registry 或 registry v2 contract。

### 15.2 忽略目录派生运行

```text
.artifacts/i18n/quality/selection-runs/
  <run>-challenge/ | <run>-dev/ | <run>-holdout/
  run-manifest.json / raw-output.json / assessment.json / report.json
```

### 15.3 受保护 holdout 材料与可见性

- Holdout 的 **exact revision IDs、可恢复成员映射、source/target/context payload、stratum/clean 标签、findings/adjudication** 全部为受保护材料：**永不进入版本控制**，存放在忽略目录或项目外受保护存储，以 SHA-256 manifest 记录身份（沿用 Facts A-core 归档模式）。版本控制仅保存不可逆 commitment/总数/配额与 hash（§6.5、§15.1）。
- Dev/Challenge 的精确 revision IDs 与 Challenge 成员可公开，并在版本控制中明文保存。
- **受保护 master asset 的读取方**：exact IDs/mapping/full payload/labels 的 master asset 仅由 **ORCHESTRATOR 的冻结 dispatch builder**（为 S8/S9 组装当块 envelope）与**决策函数**按阶段读取。
- **候选 REVIEWER 的读取**：S8/S9 的 REVIEWER **必须**通过当前 envelope 看到当块的 source/target/context（否则无法评估），但除当前 envelope 及其明确引用的公开源码片段/结果 schema 外，**不得读 master asset、labels、其他条目/块、registry 或 inventory**；路由输出先密封，再由决策函数揭示对应 labels 计分。按 envelope-only 边界验证（§4.3、§13）。

### 15.4 设计级命令占位（未实现，禁止调用）

```text
python3 -B tools/i18n quality selection-*   # 仅设计占位；未实现，不得调用
```

任何选择执行必须走 §4.1 的 Paseo 路由链，不因占位命令存在而产生新的执行路径。

### 15.5 三类资产分离与 Holdout 可见性

版本控制的规范性资产、忽略的派生运行、受保护 holdout 材料三者不得混放；派生运行
不得写入规范目录，规范资产不得被运行结果覆盖。

- 版本控制可见：不可逆 set commitment、总数、六层配额、contract/hash；Dev/Challenge 的精确 revision IDs 与 Challenge 成员可明文。
- 严格受保护（永不进版本控制）：Holdout 的 exact revision IDs、可恢复成员映射、payload、stratum/clean 标签、findings/adjudication；不得以任何形式写入版本控制、日志或可浏览产物中。

## 十六、仓库措辞澄清（DD16）

当前仓库相关措辞按以下方式澄清（本协议不修改任何既有文档，只在本协议范围内给出
规范读法）：

1. **活跃 `translation_contextual_v1` 是运行时解耦的**：它绑定 `role=reviewer` +
   `purpose=translation_contextual_v1`，运行时载体由 ORCHESTRATOR 按当前环境选择，
   契约不固定 provider/model/档位。因此**活跃契约没有固定 DeepSeek**。
2. **第二评估器未定的真实原因**：缺少 (a) selection identity（候选路由身份与选择
   样本身份）、(b) 授权（选择执行与外部传输授权）、(c) 生产映射（选择结果如何映射到
   生产评估器配置）；**不是因为活跃契约固定了 DeepSeek**。
3. 早期运行记录中“新通道目前只固定 DeepSeek 一个译文 reviewer”一类表述只是
   对当时运行配置的观察，不构成契约绑定；本协议按 §1–§4 与本节语义取代该语境下的
   推断。
4. 本协议不把任何模型身份写入契约：候选路由身份全部是预注册值（§17）。

## 十七、协议固定值 vs 预注册固定值

### 17.1 协议固定值（本文件冻结；修改须走 infrastructure 变更审核）

- 全部尺寸：**preselection frame cap=320（protocol-frozen，非 dataset，不登记 registry）**；final pool 160（从 frame ≤320 中按冻结顺序精确选出）；Dev 80；Challenge 24 ⊆ Dev（只用于筛选，指标不计入最终性能报告；从已裁决 Dev 中按 6/3/3/2/2/8 含 8 strict-clean 冻结；≥8 substantive 且 ≥4 decision-changing 否则停止，见 §6.3）；Dev clean/acceptable 24；Holdout
  80 = Primary 40 + Extension 40（每块 10/5/5/4/4/12=40，pooled 20/10/10/8/8/24，见 §6.4）；Holdout clean 24 = Primary 12 + Extension 12；
  初始路由 6–10；Challenge 收缩后最终前沿 3–4（<3 立即停止，3–4 全进 Dev，>4 按四端点 Pareto＋字典序到 4，含可估计性检查，见 §11.3）；Dev survivors 最多 4（<2 停止）；finalist 2；
- 执行次数：Challenge 与首次 Dev 各一次/适用路由；仅 finalist 第二次独立 Dev；
- 六层主层配额与分块：Dev 20/10/10/8/8/24；Holdout 10/5/5/4/4/12×2=80；Challenge 6/3/3/2/2/8=24；互斥主层，次级标签可重叠；四类身份中 route 不含 dispatch，见 §12.1；
- 排除规则（registry + exclusions）、S1.5 人工 preliminary stratification（route-blind/output-blind、target-visible，不允许 AI label）与 fail-closed 语义；Challenge 成员随样本冻结、不可事后调整；
- 术语 `human-adjudicated selection set`；禁止 certification Gold 措辞；
- 选择状态四态与分母排除规则；原子 finding 字段；
- 端点定义与公式（recall ×2、clean FP、review_burden、false_findings_per_100、
  次级/操作端点）；禁止不透明总分；
- 匹配规则与 false finding/scope violation 语义；
- 优势界（+10pp、+10pp、−8pp、−0.10）与非劣界（−5pp、−5pp、−0.05）；decision-changing 定义为满足任一：(a) changes_rule_understanding=yes 且 can_change_player_action=yes，或 (b) required_operation_info_missing=yes；
- paired bootstrap：冻结主层内的 paired stratified item bootstrap，固定 seed、2000 replicates、有效 replicate 的 95% percentile interval；原始分母（人工裁决参考分母）为 0 则端点不可用于优势，replicate 分母 0 记 undefined 并排除，有效 replicate <95% 则端点不可用于优势；**non-inferiority 需单侧 95% bound（名义 .05）支持界值**，不可估计时该方向失败；每个端点独立用 95% interval 判定，不做多重比较校正（见 §10.2/§10.5）；
- **Challenge 可估计性门槛**：Challenge 24 固定组成与 ≥8/≥4 issue 门槛，见 §6.3；四端点仍不可估计的路由不具备排序资格；
- tie-break 顺序（decision-changing recall → clean FP → review burden → substantive
  recall → route ID）；
- 停止规则（Challenge 最终前沿 <3 立即停止、Dev 最终前沿 <2 停止）与"不降低阈值"；Challenge 与 Dev 阶段各自整体资格门＋Pareto 后再清点最终前沿，前沿 >4 才字典序到 4；
- reveal 语义（Primary 先行；仅无结论才在 pooled 80 从头重算同一规则；Extension 单独无结论）；
- 阶段机 S0–S10（含 S1.5 人工分层）、Holdout 保密边界与 envelope-only 读取边界（§4.3、§13、§15）；隔离墙全部条款；
- run manifest 最低字段（分离 route/run_config/execution 身份，见 §12.2）与 §12.1 四类身份定义；版本不可得时的结论边界；
- **stability 为强制生产准入门槛**：阈值预注册，任一 finalist 未过则停止、无 Holdout、不递补；
- 非流行率声明。

### 17.2 预注册固定值（S0.5 sampling + S2.8 execution，两阶段冻结；任何路由输出之前）

- **S0.5 sampling preregistration（S1 前冻结）**：eligible universe（inventory/registry/exclusion identities）、确定性 source/risk 排序与 frame cap 320、人工分层表单/盲法与逐层选择 recipe、S2 deterministic allocation recipe（含向 Dev 与 Primary/Extension 的分层分配）、六层配额与失败语义；已在 S1/S2 使用的 sampling seed 不得事后称为预注册；frame 不登记 registry、不算 selection dataset.
- **S2.8 execution preregistration（S2.5 后、S3 前冻结）**：
  - 已产生的 Dev/Challenge 精确 revision IDs 与 Holdout 不可逆 commitment/总数/配额与 hash（Dev/Challenge 可明文；Holdout 不含 exact IDs/mapping）；
  - requested routes 的**具体数量**（在 6–10 内）与各 requested 路由身份（路由名/请求 provider/model/参数）及预期解析规则、允许的 identity 缺失策略与 mismatch fail-closed policy（归 route identity，不含 dispatch，见 §12.1）；**实际观测的 provider/model/version 不在 S2.8 预冻结，按 §12 manifest 记录并校验，超出允许解析范围则 fail closed**；
  - bundle/prompt/terminology/source 的精确 hash 与 bytes（归 bundle/run_config，非 route）；run numbers；dispatch/attempt/timestamps 归 execution identity（§12）；bootstrap seed；
  - selection purpose 名称已由协议固定为 `evaluator_selection_v1`（§4.3），但激活需另行基础设施修改；selection result contract 的版本/identity/hash 由未来版本化规范资产固定，preregistration 仅绑定其 identity/hash；
  - Dev clean/acceptable 层内 strict-clean 的精确数量（≥12 下限之上）与四类身份的精确 bytes/hash；
  - latency/cost 预算与任何附加操作门槛（可增加，不得放松 §11.1 最低项）；
  - **stability 阈值数值**（§8.3，强制门槛，S2.8 前预注册，门槛本身为 protocol-frozen）。

## 十八、解释性填充与假设

SPEC 未完全指定处，本协议作如下显式填充（reviewer 可据此核验一致性）：

1. **Challenge ⊆ Dev**：池 160 = Dev 80 + Holdout 80 无独立空间，故 Challenge 24 是
   Dev 的固定视图，从已裁决 Dev 中按 6/3/3/2/2/8（含 8 strict-clean）冻结；Challenge 指标只用于漏斗筛选，不计入 Dev/Holdout 最终性能报告；survivor 的 Dev 评分仍覆盖全量 80。
2. **review_burden 分母**：`evaluated revisions` 定义为 evaluated set 中
   `clean`/`defect` 状态条目（`context-insufficient`/`source-issue` 按 §7.4 排除），
   与分子（false findings）保持同口径。
3. **Holdout clean 平衡**："24 clean/acceptable 总量，Primary/Extension 12/12 clean"
   读作：Holdout 中 24 条 clean/acceptable 全部为 strict-clean，Primary 12 + Extension
   12；Dev 的 24 条 clean/acceptable 层在样本冻结时固定 strict-clean 子集且 ≥12，
   以与 Holdout 保持可比（下限属协议固定值，精确数量预注册）。
4. **unmatched false findings** 即 false findings（未匹配 substantive finding ＋ 一切被禁
   presentation/style finding。
5. **selection purpose 名称已由协议固定为 `evaluator_selection_v1`**（§4.3、§17.1），但本文件仅设计、尚未激活；激活前须另行修改 AGENTS/.ai roles/Paseo contract 与门禁并经基础设施交叉审核；selection result contract 的版本/identity/hash 由未来版本化规范资产固定，preregistration 仅绑定其 identity/hash；envelope-only 精确读取边界见 §4.3 与 §13。
6. **stability 为强制生产准入门槛**：门槛本身 protocol-frozen，阈值数值在首个候选输出前预注册；任一 finalist 未过则停止、无 Holdout、不递补。

## 十九、验收与符合性

本文件作为延期设计参考满足：

- 自包含、规范性，足以供独立 REVIEWER／SENIOR_REVIEWER 交叉复审；
- 明确区分协议固定值与预注册固定值（§17）；
- 全部计数自洽（§5 一致性核对）且 Primary/Extension reveal 语义无歧义（§10.6）；
- 不声称选择数据是 Gold、流行率证据、生产准入或已实现功能（§7.1、§8.4、§14、§15）；
- 不引入直接 provider 或已退役 runner 执行路径（§4.2）；
- 不声称 contract foundation、schema、validator 或测试已经落地。pre-Lite 全量实现资产已按
  [`evaluator-selection-full-impl-discard-manifest.md`](evaluator-selection-full-impl-discard-manifest.md)
  全部丢弃；未来若满足升级条件，必须从新的独立任务重新实现和审核。

本文档修改时的门禁：

- `git diff --check -- docs/translation-quality-evaluator-selection-v1.md`；
- `python3 -B tools/paseo_contract_check.py`。

仓库中不存在 `tests/i18n/test_quality_selection.py` 或对应全量实现测试；不得把历史 pre-Lite
测试结果当作当前门禁。

## 二十、参考文档

- `AGENTS.md`：编排、门禁、外发与判定依据；
- `docs/paseo-orchestration-v2-contract.md`：角色、状态机、恢复与 review 记录；
- `docs/paseo-translation-context-review-v1-contract.md`：活跃译文语境审核契约（本协议
  不修改）；
- `docs/translation-quality-system.md`、`docs/translation-quality-evaluator-v2.md`、
  `docs/translation-quality-evaluator-v3.md`：历史质量设计（本协议不重解释）；
- `docs/translation-quality-facts-study-v1.md` / `v2.md` / `report-v1.md`：Facts 研究
  （保持原样）；
- `docs/translation-quality-offline-closure-plan.md`：数据集登记与 curation 治理模式；
- `i18n/quality/README.md` 与质量系统文档：正式 120 条 / M5 / M6 / Gold-Silver TM 的 deferred 状态（本协议不以未跟踪的 `docs/project-roadmap.md` 作为规范依据）；
- `i18n/quality/dataset-registry-v1.json` 与 `i18n/quality/facts-study-exclusions-v1.json`：
  权威排除来源。
