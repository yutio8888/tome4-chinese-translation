# 翻译质量 Evaluator Layer v1 设计

> **状态：仅设计／SPEC，未实现、未激活。** 当前唯一活跃的译文审核路由仍是
> `role=reviewer`、`purpose=translation_contextual_v1`。本文不授权创建 Paseo child、调用
> provider、外发译文 bundle、抽样或人工标注，也不授权新的 purpose、生产路由、自动修复、
> Gold／Silver／TM、commit、push 或 release。
>
> 本设计描述未来如何在不改变现有审核责任边界的前提下增加 evaluator 层。实际实现必须成为
> 独立任务；若修改 `AGENTS.md`、角色定义、Paseo 契约或质量工具，须按仓库规则完成独立
> REVIEWER 与 SENIOR_REVIEWER 交叉复审及适用门禁。

## 一、结论与定位

Evaluator Layer 不是另一个拥有裁决权的 reviewer，也不是自动放行器。它由一条独立、盲评、
只读的模型评估通道和一组宿主侧确定性控制组成，用于：

1. 为现有语境审核补充独立的缺陷发现信号；
2. 识别 reviewer／evaluator 分歧、上下文不足和重复运行不稳定；
3. 在预先冻结的预算内触发额外复审，而不是自动确认问题；
4. 测量漏检、误报、人工负担、稳定性、延迟和成本；
5. 为 evaluator 选型、版本漂移监控及未来质量试点提供可重算证据。

模型输出始终只是 observation／finding proposal。源码事实、finding 是否成立、severity、修复
范围和批次终态继续由 ORCHESTRATOR 按固定源码与项目政策裁决；只有 `confirmed` finding 可
进入 EXECUTOR 修复。

## 二、架构

```text
冻结候选 revision
        │
        ├── 确定性门禁
        │     lint / runtime / collision / diff / tests
        │
        ├── Paseo REVIEWER
        │     purpose=translation_contextual_v1
        │     → observation + exact source/target evidence
        │
        └── 未来 Paseo REVIEWER
              purpose=translation_evaluator_v1
              → structured assessment
                     │
                     ▼
             宿主严格校验、规范化、匹配
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
   ORCHESTRATOR 源码裁决      质量、负担与漂移报告
         │
         ▼
  保持原流程 / 追加复审 / EXECUTOR 修复
```

概念上增加 evaluator 层，但不新增 Paseo canonical role。未来运行仍使用只读 `REVIEWER`，通过
独立 `purpose` 绑定行为。`translation_evaluator_v1` 在本文中只是候选名称，不因文档存在而
获得 runtime、STATE、外发或 provider 权限。

### 2.1 两个平面

Evaluator Layer 分为两个互相隔离的平面：

- **运行平面**：对当前冻结候选执行独立评估，返回最小结构化 assessment；
- **控制平面**：验证身份和覆盖、规范化 finding、匹配人工裁决、应用路由政策、生成指标并
  监控配置漂移。

模型只存在于运行平面。控制平面必须是本地、确定性、可测试的宿主实现；它不能调用模型猜测
缺失字段，也不能把解析失败解释为 clean。

## 三、职责和禁止事项

| 组件 | 负责 | 不负责 |
|---|---|---|
| Contextual REVIEWER | 常规逐条语境审核，返回 observation 和冻结证据 | evaluator 校准、最终定级 |
| Evaluator REVIEWER | 独立发现实质语义问题，返回结构化差异和证据 | severity、确认、修复、放行 |
| 宿主工具 | 严格校验、span 规范化、问题匹配、指标和路由派生 | 猜测缺失语义、修改模型 finding |
| ORCHESTRATOR | 固定源码核验、事实裁决、severity 和路由决定 | 按模型身份或多数票裁决 |
| EXECUTOR | 修复已确认且在范围内的 finding | 根据 evaluator 输出自行扩张范围 |

Evaluator Layer 永远不得：

- 替代现有 lint、runtime key、collision、markup、placeholder 或构建门禁；
- 因 reviewer 与 evaluator 同时返回 clean 而自动接受译文；
- 把 evaluator finding 自动标成 `confirmed` 或直接生成修复任务；
- 让模型填写 severity、grade、Gold／Silver、reuse／TM eligibility 或最终 score；
- 把两个模型的多数票当作源码或人工裁决；
- 读取另一 reviewer 的输出、历史 finding、裁决、期望答案或建议修复；
- 在模型、prompt、policy 或输入身份变化后沿用旧校准结论。

## 四、候选与执行身份

### 4.1 同源但不同 envelope

Contextual reviewer 与 evaluator 必须来自同一冻结候选事实：相同有序 revision、source、target、
`source_tag`、固定源码身份、术语快照和有界语境。两条通道分别投影自己的 envelope，不能共享
结果或把一方的输出注入另一方。

候选 envelope 建议沿用“payload + hash identity”模式：

```json
{
  "candidate_identity": "<sha256(canonical payload bytes)>",
  "payload": {
    "contract": "translation_evaluator_v1",
    "ordered_revision_ids": ["..."],
    "fixed_source_identity": "...",
    "translation_snapshot": [
      {
        "revision_id": "...",
        "source": "...",
        "target": "...",
        "source_tag": "...",
        "profile": "mechanics"
      }
    ],
    "bounded_context": [
      {"revision_id": "...", "context": "..."}
    ],
    "terminology_snapshot": "...",
    "rendered_briefing": "..."
  }
}
```

以上只是未来 schema 的设计形状，不是已经生效的 contract。实现时必须冻结规范 JSON 规则、
精确字段集合、类型、字节上限、文件上限和 hash recipe，并对所有额外字段 fail closed。

### 4.2 requested／observed 分离

模型不能自行声明可信的 provider、model、thinking、prompt hash 或运行身份。宿主在模型输出
之外维护运行记录，至少包括：

- `task_id`、`dispatch_id`、workspace 和 parent lineage；
- requested provider/model/thinking/parameters；
- observed exact model identity 与 Paseo receipt；
- candidate、prompt、policy、result-shape 和 envelope hash；
- 开始／结束时间、延迟、成本、缓存状态和失败类别。

requested 与 observed 不精确相符、实际身份不可核验、dispatch 迟到或候选已变化时，整个输出
无效。不得由 provider 名、profile 名、title、记忆或枚举推断 exact model identity。

### 4.3 读取与写入边界

Evaluator REVIEWER 必须 fresh、只读、无历史会话，并只读取：

1. 当前冻结 evaluator envelope；
2. 固定 result-shape bytes；
3. envelope 逐项明确引用且已授权外发的公开源码路径。

隐藏 reference label、人工裁决、另一 reviewer 输出、历史 assessment、样本 master 和其他阶段
bundle 必须位于 allowlist 之外。派发前后都要验证 reviewer 没有改变 HEAD 或工作树中的任何
路径。无法证明读隔离或只读语义时不得发送输入。

## 五、模型输出

### 5.1 最小结果形状

未来 `translation_evaluator_v1` 的最小输出建议为：

```json
{
  "contract": "translation_evaluator_v1",
  "candidate_identity": "<sha256>",
  "items": [
    {
      "revision_id": "<sha256>",
      "assessment_state": "assessed",
      "findings": [
        {
          "finding_id": "E-001",
          "error_family": "accuracy",
          "phenomenon": "number-range",
          "meaning_change": "strengthened",
          "source_evidence": {
            "quote": "3–8 damage",
            "occurrence": 1
          },
          "target_evidence": {
            "quote": "8点伤害",
            "occurrence": 1
          },
          "explanation": "浮动范围被表达成固定上限",
          "impact_facts": {
            "changes_rule_understanding": "yes",
            "can_change_player_action": "yes"
          }
        }
      ]
    }
  ]
}
```

允许的 item state 至少区分：

- `assessed`：完成评估；`findings=[]` 只表示该 evaluator 没有报告实质问题；
- `context-insufficient`：给定语境不足，不能解释成 clean；
- `source-issue`：原文／源码本身存在阻碍评价的问题，不能解释成译文错误。

`error_family`、`phenomenon`、`meaning_change` 和 `impact_facts` 都必须使用版本化白名单；
`impact_facts` 只允许可观察的三态事实，例如 `yes|no|unknown`，不允许自由 severity。

### 5.2 严格校验

以下任一情况使整个 assessment 成为 `invalid-execution`：

- contract、candidate、dispatch 或 exact model identity 不匹配；
- item 数量、顺序、集合或 revision identity 与 envelope 不一致；
- 少项、多项、重复、重排或只返回部分 shard；
- 出现未声明字段、非法枚举、空 explanation 或宿主专属字段；
- source／target evidence 无法唯一解析到冻结字节；
- 捏造 envelope 未提供的上下文或源码事实；
- 返回 presentation-only／纯风格 finding；
- reviewer 写入工作树或输入在运行期间发生变化。

无效输出、原始响应、失败类别、成本和延迟仍要保留；不得删除失败、放宽 schema、用部分输出
补成 clean，或因结果不理想而更换样本。

## 六、Contextual 结果桥接

### 6.1 为什么不能直接映射

当前 `translation_contextual_v1` 每条 revision 只有 `observation` 和完整 source／target evidence，
且禁止 reviewer 填写 severity、确认状态或其他字段。自由文本 observation 不能确定性推导
`error_family`、`phenomenon`、`meaning_change`、span 或影响事实。

因此禁止：

- 用关键词把 observation 自动分类；
- 让另一个模型补写结构化字段；
- 把任意非 `OK` observation 自动视为 confirmed finding；
- 为满足旧 v3 schema 而伪造 `context_sufficient` 或 evidence span。

### 6.2 两阶段桥

建议增加宿主拥有的 `contextual-disposition-v1` 裁决记录：

```text
translation_contextual_v1 result
        │
        ▼
ORCHESTRATOR disposition
  - confirmed / pending / advisory
  - error family / phenomenon / meaning change
  - normalized source and target evidence
  - impact facts
  - fixed-source verification reference
        │
        ▼
normalized quality finding
```

具体规则：

1. `observation == "OK"` 只记录“该 reviewer 未报告问题”，不是人工 clean truth；
2. 非 `OK` observation 必须逐条绑定 disposition，不能遗漏或静默丢弃；
3. `confirmed` finding 缺少结构化类别、证据或适用的源码核验时，桥接失败；
4. `pending` 保持未决，不能降级成 clean，也不能进入自动修复；
5. `advisory` 保留用于负担和误报分析，但不进入 confirmed defect 指标；
6. 只有完整、经验证的 disposition 才能投影为后续 assessment／finding／match artifact；
7. 桥接必须绑定 contextual candidate、dispatch、result hash 和 adjudication hash。

这条桥既不改变 `translation_contextual_v1` 的三键结果，也不重解释历史 v3 artifact。未来若要
解除 P4 route incompatibility，必须建立新的 preregistration 和显式版本映射，不能修改历史
冻结文件来迁就新路线。

## 七、Finding 规范化与匹配

### 7.1 规范化

宿主对每条有效 finding 确定性派生规范签名：

```text
revision_id
+ error_family
+ phenomenon
+ meaning_change
+ normalized source evidence
+ normalized target evidence
```

规范化只处理 Unicode、quote occurrence、whole-item 表示、span 和已冻结兼容表；不能改写
explanation 或推断新的语义事实。相同输入和规则版本必须产生相同签名。

### 7.2 匹配

匹配只在同一 `revision_id` 内进行。候选边至少要求：

- error family／phenomenon 按版本化兼容表可匹配；
- source 或 target evidence 精确相同或有足够 span overlap；
- meaning change 不互斥。

多个 finding 的拆分／合并采用现有质量设计中的二部图思想。唯一最优匹配可以由宿主生成；
并列、互斥或证据不足时进入人工裁决，不能强制配对。模型未匹配 finding 不自动等于误报，
人工已确认但模型未匹配的 issue 才能计为漏检。

所有质量指标都以候选输出之前冻结的真实人工／源码裁决为 reference；contextual reviewer 和
evaluator 不能互相充当真值。

## 八、路由政策

### 8.1 基本矩阵

| Contextual reviewer | Evaluator | 宿主动作 |
|---|---|---|
| 无 finding | 无 finding | 继续现有流程；不得因双 clean 自动放行 |
| 有 finding | 无 finding | 正常源码裁决；evaluator 不得降低 finding |
| 无 finding | 有新 finding | 冻结基线后由 ORCHESTRATOR 核验；confirmed 才修复 |
| 描述同一问题 | 描述同一问题 | 匹配为一个 issue，保留两个来源和各自原始文本 |
| 实质结论冲突 | 实质结论冲突 | 追加独立复审；不多数表决 |
| 任意 | `context-insufficient` | 按 profile／风险预算追加语境，不解释为 clean |
| 任意 | invalid／missing | SHADOW 记失败；ROUTE_ONLY 回退现有完整审核 |
| 任意 | 重复运行不稳定 | evaluator 降级为 SHADOW，不参与自动路由 |

Evaluator 的唯一生产权限是“请求额外关注”。它不能跳过 contextual final full review、降低
已有 finding、改变五步门禁、直接驱动 EXECUTOR 或完成 `DONE_VERIFIED`。

### 8.2 路由信号

进入 `ROUTE_ONLY` 后，可以触发额外复审的信号包括：

- evaluator 独有的 decision-changing 候选 finding；
- reviewer／evaluator 对 polarity、condition、number-range、entity-role、omission 等实质问题
  有分歧；
- `context-insufficient` 且 profile 为 mechanics、runtime-adjacent 或高暴露 UI；
- 同一配置重复运行的 item state 或 normalized finding 差异超过预注册边界；
- exact model、prompt、policy、schema、上下文 recipe 或依赖版本漂移；
- invalid-execution rate 或人工负担超过冻结预算。

路由预算、优先级和阈值必须在观察结果前冻结。预算耗尽时按确定性的风险顺序选择追加复审，
不能根据模型品牌或主观信任选择。

## 九、运行状态

运行政策只允许以下状态：

```text
OFF → SHADOW → ROUTE_ONLY
       ▲           │
       └───────────┘  identity drift / health failure / evidence regression
```

### 9.1 OFF

没有 evaluator dispatch、外部传输或生产影响。离线 schema、validator、fake replay 和历史
artifact 读取测试可以存在，但不产生质量结论。

### 9.2 SHADOW

- evaluator 与 contextual reviewer 对同一候选互盲运行；
- 在揭示 evaluator 输出前冻结 `baseline_decision_id` 和原审核结论；
- evaluator 不能自动改变批次状态或追加 child；
- 新 finding 仍由 ORCHESTRATOR 核验，避免明知实质问题却忽略；
- 对比时分别报告“原流程结果”和“evaluator 增量发现”，防止事后污染基线；
- 收集 invalid rate、增量确认率、误报负担、稳定性、延迟和成本。

### 9.3 ROUTE_ONLY

只有在预注册选择、隐藏确认和外发授权完成后，evaluator 才能按冻结政策请求额外复审。
`ROUTE_ONLY` 仍不授予自动确认、severity、自动修复、Gold／Silver／TM 或自动接受权限。

本设计没有 `AUTO_ACCEPT` 或 `AUTO_FIX` 状态。若未来需要无 mandatory human review 的自动
修改，必须按 Selection-Lite 的升级条件创建新的完整基础设施决策，不能扩写本 contract。

## 十、指标与选择

### 10.1 决策顺序

选择和晋级不得使用不透明总分。结果出现前按以下顺序冻结：

1. correctness／safety gates；
2. decision-changing miss；
3. false findings；
4. human review burden；
5. stability；
6. latency／cost。

主指标至少包括：

```text
decision_changing_miss_rate
  = missed adjudicated decision-changing issues
    / adjudicated decision-changing issues

false_findings_per_100
  = 100 * unmatched substantive findings
    / evaluated revisions

human_review_burden_per_100
  = 100 * findings requiring human disposition
    / evaluated revisions
```

重复运行还要报告：

- item-state exact agreement；
- normalized finding Jaccard；
- invalid-execution rate；
- 按 mechanics／narrative／UI 等 profile 的分层结果；
- evaluator 独有 confirmed finding 数与确认率；
- 额外复审触发率、延迟和成本。

所有比例同时报告原始分子／分母和不确定性。若 decision-changing 分母不足或样本过少，必须
报告“证据不足”，不能用 100% 或零漏检宣称可靠。

### 10.2 与 Selection-Lite 的关系

`evaluator_selection_v1` 负责在未来另行授权后，从 3–4 个预登记候选配置中选择生产候选；
`translation_evaluator_v1` 描述被选择配置在日常批次上的未来运行行为。两者 purpose、样本、
ledger 和权限必须分开，选择结果不会自动激活生产 purpose。

生产选择只使用 `real-adjudicated` 自然 revision。`controlled-artificial` 只做错误现象诊断和
execution gate；`fake-replay` 只测试 parser／validator，二者都不能进入生产选择指标。

当前 Selection-Lite 的 Dev-32、Top-2 重复运行、隐藏 Primary-32／可选 Extension-32、practical
margin 和结论规则保持独立权威。本文不改写其样本、阈值或授权状态。

## 十一、Artifact 与证据边界

可重生成的运行数据建议写入：

```text
.artifacts/i18n/quality/evaluator-layer/runs/<run-id>/
  envelope.json
  dispatch-record.json
  raw-result.json
  validated-assessment.json
  normalized-findings.json
  comparison.json
  report.json
```

含人工判断、不可重建核验锚点或晋级决定的证据才进入受跟踪路径：

```text
evidence/quality/evaluator-layer/
  preregistration/
  sample-manifests/
  adjudications/
  source-verifications/
  promotion-decisions/
```

原始模型输出不能直接进入权威质量配置，也不能修改 `i18n/quality/` 下历史 policy、schema、
anchor、preregistration 或 report 的含义。受跟踪证据必须绑定 `tu_uid`、`revision_uid`、
`revision_id`、source/target bytes、固定源码 provenance、candidate identity 和裁决 revision。

## 十二、分阶段实施

### P0：离线契约与 replay

目标是不调用 provider 即验证数据闭环：

- 新建 evaluator envelope／result／run-record／disposition／comparison schema；
- 实现 canonical identity、严格 validator、规范化、匹配和报告；
- 用 `fake-replay` 覆盖 clean、finding、context-insufficient、invalid 和分歧案例；
- 验证输入不变、额外字段拒绝、coverage、evidence occurrence、迟到结果和身份漂移；
- 本地 CLI 只能构建、校验、匹配和报告，不能直接调用 provider。

P0 完成不产生运行义务，也不激活任何 purpose。

### P1：SHADOW MVP

另行授权并完成基础设施复审后：

- 激活 `role=reviewer`、`purpose=translation_evaluator_v1`；
- 在 STATE 中使用独立 evaluator record，不能满足 contextual review completion；
- 通过 Paseo fresh child 执行，禁止 direct-provider 或 retired blind runner fallback；
- 冻结 baseline decision 后再揭示 evaluator 结果；
- 只生成增量发现、负担、稳定性、失败和成本报告。

### P2：Selection-Lite

- 盘点 append-only evidence pool；
- 只从 eligible `real-adjudicated` revision 冻结候选 frame；
- 按现有 Lite 设计执行 Dev、Top-2 重复运行和隐藏确认；
- 第二 evaluator/provider/model 与 bundle 外发范围必须单独授权；
- 无有效比较、样本不足或 marginal value 不足时允许不选 winner。

### P3：ROUTE_ONLY

只有以下条件全部满足才可从 SHADOW 晋级：

1. exact provider/model/prompt/policy/schema identity 已冻结；
2. fail-closed contextual disposition 与质量 bridge 完整覆盖；
3. 隐藏确认支持当前配置，且没有 correctness／safety gate 失败；
4. 人工额外复审负担处于预注册预算内；
5. 第二独立 evaluator 或正式质量试点所需独立性已授权；
6. 漂移、失败和降级路径经过离线回放测试；
7. 不改变 contextual final full、五步门禁和 `DONE_VERIFIED` 语义。

任一身份变化、健康失败或真实运行证据回归都自动降回 SHADOW；不能沿用旧 clearance。

### P4：正式质量试点（仍延期）

正式 120、M5／M6、Gold／Silver／TM 仍受当前路线图的四项解除条件约束：新 preregistration、
fail-closed 映射、第二独立 evaluator 与外发授权、人工先标注分层正负对照集。完成 P0–P3 中
任何一项都不会自动解除这些条件。

## 十三、预计实现面

未来实现预计触及：

- 新的 evaluator 设计契约和 `i18n/quality/schemas/` schema；
- `.ai/roles/` 中 REVIEWER purpose 分支；
- Paseo 契约、STATE evaluator records、恢复／归档／只读语义；
- `tools/i18n quality evaluator-*` 的离线构建、校验、匹配和报告命令；
- contextual disposition 到 normalized quality finding 的 fail-closed bridge；
- `tools/ai_state_check.py` 和 `tools/paseo_contract_check.py` 的对应约束；
- schema、identity、coverage、matching、routing、drift 和 no-input-mutation 测试。

实现时应创建 fresh versioned artifact，不能恢复已退役 blind runner，也不能原地修改历史 v3
artifact。现有 v2/v3 代码只有在纯宿主逻辑、contract 语义完全兼容且有回归测试证明时才可
复用；否则应使用显式 adapter 或新版本实现。

## 十四、验收原则

Evaluator Layer 的成功标准不是“模型给出的评分更高”，而是：

- 在真实裁决数据上补充发现 decision-changing issue；
- 没有降低现有 reviewer、源码裁决和确定性门禁的保护；
- 误报与额外人工工作处于预注册预算内；
- 重复运行、模型身份和版本漂移可测量、可降级；
- 每个决定都能从冻结输入、原始输出、宿主规则和人工裁决重算；
- evaluator 失效时，系统回到现有保守审核路径，而不是把失败解释为通过。

如果 evaluator 的边际收益低于直接修复译文，应保持 OFF／SHADOW，优先推进译文主线，而不因
已经投入基础设施成本强行晋级。

## 参考

- [`paseo-translation-context-review-v1-contract.md`](../../docs/paseo-translation-context-review-v1-contract.md)
- [`paseo-orchestration-v2-contract.md`](../../docs/paseo-orchestration-v2-contract.md)
- [`translation-quality-evaluator-v2.md`](translation-quality-evaluator-v2.md)
- [`translation-quality-evaluator-selection-lite-v1.md`](translation-quality-evaluator-selection-lite-v1.md)
- [`translation-quality-system.md`](../../docs/translation-quality-system.md)
- [`project-roadmap.md`](../../docs/project-roadmap.md)
- [`../i18n/quality/README.md`](../../README.md)
