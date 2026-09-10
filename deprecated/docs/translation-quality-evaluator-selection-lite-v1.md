# 翻译质量评估器选型 Selection-Lite v1

> **状态：仅设计／SPEC。** 本文件只定义一个未来可实现的轻量选型方案；仓库中不存在、
> 也未授权其实现或 campaign。`purpose=evaluator_selection_v1` 保持 **inactive**。
>
> 本文件不授权候选 evaluator／provider 调用、抽样、人工标注、外部传输、purpose 激活、
> 生产配置映射、Gold／Silver／TM 权限、commit、push、release，也不授权正式 120 条、
> M5／M6 或 v3 calibration。任何这些动作都必须成为后续独立任务并重新取得授权。
>
> 完整协议仅为
> [`design-reference / full protocol deferred`](./translation-quality-evaluator-selection-v1.md)，
> 不是 Lite 的实现基线或待办。Selection-Lite 有意把渐进证据挂接到日常小批次译文循环，
> 这一点不同于延期的完整协议。

本文面向单维护者个人项目的一次可逆生产 evaluator 选择。它只冻结未来决策所需的最小
语义；不建立发表级 benchmark、公共流行率估计或认证平台。文中的“冻结”“运行”“记录”
均描述未来另行授权后的行为，不表示这些动作已经发生。

## 一、定位与渐进证据

### 1.1 决策定位

Selection-Lite v1（下称 Lite）只回答：在 **3–4 个预登记候选运行配置**中，哪一个更适合
成为个人项目当前的生产 evaluator 候选。该选择：

- 是一次性的、可撤销的维护决策；后续真实使用证据可以推翻它；
- 只适用于冻结的配置、样本和观测时间，不证明某模型的一般能力；
- 不构成 benchmark 排名、语料缺陷流行率、公开比较结论、认证或发布声明；
- 不授予任何译文 Gold／Silver／TM、复用、正式 120 条或生产映射权限。

Lite 的首要目标是让选择成本服从译文主线，而不是为了选择本身建设研究设施。其主要证据
来自日常小批次译文循环的副产品：

```text
真实小批次 revision
  → Paseo REVIEWER（purpose=translation_contextual_v1）
  → 维护者按固定源码核验并裁决
  → append-only evidence pool
  → 未来另行授权的 Selection-Lite 冻结样本
```

因此 Lite 明确与[当前项目路线图](../../docs/project-roadmap.md)耦合；延期完整协议仍只作为升级时的
设计参考。

### 1.2 append-only evidence pool

未来实现可以维护一个仅追加的证据池。每个池条目至少绑定：

- 当前 `tu_uid`、`revision_uid`、`revision_id`；
- 精确 source 与 target 字节；
- component 与 source provenance（包括版本／commit、仓库相对路径或等价来源定位）；
- 维护者裁决状态；
- 第八章规定的 evidence class；
- source-verification reference，足以定位实际机制或明确“不适用”的核验记录。

池按 `revision_id` 去重：同一 `revision_id` 只保留一个池条目；source、target 或修订身份变化
产生新的 `revision_id`，新 revision 只追加，不覆盖、改写或“更新”旧历史。池记录的译文批次
裁决是候选证据来源，但 Dev／隐藏集仍按本文件规定完成与候选输出隔离的选择裁决。

模型输出永远不能提供、补写或修正 reference label。选择标签只能来自维护者语义裁决和必要
源码核验。若池不能支持已冻结的 Dev 组成，抽样必须停止；不得让受控人工构造条目静默填补
真实证据缺口。

### 1.3 64–96 候选框

未来 campaign 在看到任何候选输出前，从合格的 `real-adjudicated` 自然 revision 中按预先
冻结的 eligibility、分层和确定性顺序形成 **64–96 条有序 candidate frame**：

- 目标模式为 **96**：Dev 32 + Primary 32 + Extension 32；
- 缩减模式为 **64–95**：只能冻结 Dev 32 + Primary 32；必须在结果出现前写死
  `extension_available=false`；未使用条目不得在结果出现后扩成 Extension；
- 少于 64 条，或无法满足 Dev 的精确组成，立即停止；
- 多于 96 条时，仅按预冻结顺序／recipe 取有界的 96 条，不因候选结果调整 frame；
- frame 为 65–95 条时，样本 recipe 仍只冻结 64 个 Dev／Primary 身份；其余条目不构成
  备用样本、替补或事后扩容来源。

三块之间不得重叠，且都绑定冻结时的当前 revision 字节。任何后续 revision 变化都不能原地
替换样本，只能使该 campaign 停止或在新授权下建立新候选。

## 二、决策策略

### 2.1 结果前冻结的顺序

在看到任何候选结果前，`protocol` 必须依次冻结以下决策顺序；运行中不得改序：

1. correctness／safety gates；
2. decision-changing miss 比较；
3. false findings 与 human review burden；
4. stability；
5. latency／cost（最后才使用）。

同一层含两个指标时按列出顺序比较；前一个指标没有形成结论才看后一个。某层差异未达到
实用界并不等于质量相同，只表示继续下一指标或下一阶段。禁止不透明总分、事后加权或按结果
挑选指标。

### 2.2 correctness／safety gates

每次候选执行必须同时满足：

1. 执行完成且输出可按冻结 result shape 严格解析；
2. 第三章的 requested／observed identity 比较成功；
3. 按冻结顺序精确覆盖全部 revision，不多、不少、不重排、不重复；
4. 每条 source／target evidence 都能解析到 bundle 中冻结的精确字节；
5. 没有 presentation-only／纯风格 finding；
6. 没有捏造 bundle 上下文或源码事实；引用的源码事实能解析到 envelope 明确提供的证据。

任一门失败使本次执行成为 `invalid-execution`。原始输出、失败类别、成本和延迟仍须保留并
计数；不得删除失败、重跑内容错误、放宽门槛或换样本。

Paseo orchestration retry 与 campaign execution 严格分离。transmission acceptance 的唯一权威
证明是 Paseo 持久化的 dispatch receipt／status：它必须绑定 `dispatch_id`，记录明确的 acceptance
state 及对应状态时间，并能由宿主独立查询。只有该持久记录明确证明 transmission **未被接受**、
因而没有 campaign execution 时，才允许对基础设施故障重试一次。进程返回、瞬时 ack 或本地
超时都不能单独证明未接受；ack 丢失或 acceptance 无法确定时必须以
`indeterminate-transmission` fail closed，停止整个 campaign，不得重试，也不得产生 selection。
这类已证明未接受的 pre-transmission retry 只记在 Paseo orchestration 中，不进入四类 Lite
工件，不是候选证据，也不创建或消耗 campaign run number。若同一 `candidate_slot` 的初始
transmission 尝试及其唯一一次允许的基础设施重试均被持久记录明确证明未被接受，整个
campaign 必须停止且不得产生 `selection-decision`；该 slot 不得被省略、视为无效执行、替换
或用于以更小候选集继续，继续需要新授权的 protocol／campaign，两次尝试均不创建 campaign
execution／manifest／assessment，仍仅保留在 Paseo orchestration 记录中。

持久 receipt／status 明确证明 transmission 已接受后，该 `dispatch_id` 对应的
`execution_id` 就是不可替换的一次 campaign execution。执行中的瞬态 orchestration state
不是 Lite 工件；`run-manifest` 只能在执行到达 terminal state 后，依据持久 receipt 和可核验的
terminal evidence 一次性构造为不可变终态工件。accepted 后未完整返回或 crash 的执行，只要
receipt／evidence 足以完成终态 manifest，就必须形成失败 terminal manifest 和保留的
`invalid-execution` assessment；若无法重建一份有效 terminal manifest，整个 campaign fail closed
且不得产生 selection decision。

accepted execution 此后的 infrastructure、timeout、content、schema、identity 或 gate failure
全部保留为 `invalid-execution`，该 route 按当前阶段停止，不得重试或 replacement。因此“首次
Dev execution 失败”专指第一次有持久 acceptance 证明的 campaign execution 失败，按第四章
立即停止；它不包括有持久 non-acceptance 证明的单次 pre-transmission retry。进入 Top-2 后，
任一比较所需执行无效都会使该比较成为 `no-valid-comparison`；无效 Primary 不得靠 Extension
修补。任何阶段都不得按结果递补候选或扩大隐藏样本。

### 2.3 核心指标

对当前冻结的 evaluated set，定义：

```text
decision_changing_miss_rate
  = missed adjudicated decision-changing issues
    / adjudicated decision-changing issues

false_findings_per_100
  = 100 * unmatched substantive findings
    / evaluated revisions

human_review_burden_per_100
  = 100 * all returned findings requiring human disposition
    / evaluated revisions
```

其中：

- `evaluated revisions` 是该有效执行必须覆盖的全部冻结 revision 数；
- decision-changing issue 由候选输出之前的维护者裁决确定；若分母为 0，该轴不可判，
  继续下一轴，不得补样；
- unmatched substantive finding 由宿主按预冻结匹配规则判定；
- “requiring human disposition”包括每条需要人工接受、拒绝、拆分或合并的返回 finding；
  不得只统计最终被接受者；
- 被 gate 禁止的 presentation-only finding 会使执行无效，不能借分类方式从 burden 中隐藏。

Top-2 在同一 Dev-32 上的两次执行还必须报告：

- **item-state exact agreement**：两次 `assessment_state` 完全一致的 revision 比例；
- **normalized finding Jaccard**：先按 protocol 冻结的签名规则，把每条 finding 规范化为
  `revision_id + error_family + phenomenon + meaning_change + source/target evidence` 集合，
  再逐 revision 计算两次集合的 Jaccard，最后取 32 条的算术平均；两次均为空时该条记 1，
  仅一边为空时记 0。

### 2.4 报告与不确定性

每一指标必须同时报告原始分子／分母、点估计和适用的不确定性，不能只报百分比：

- 二项比例（包括 miss 的单候选比例和 item-state agreement）报告 Wilson 95% binomial
  interval；
- 两候选始终按同一 revision 配对，另报逐条 disagreement／count 表；
- 决策用的差值采用不重抽样的 95% **paired item-level interval**：设当前样本有 `n` 条，
  对每条构造配对贡献 `z_i`，以
  `mean(z) ± t(0.975,n-1) * sd(z) / sqrt(n)` 计算；`sd=0` 时区间退化为点；
- miss 差值令 `D` 为全部裁决 decision-changing issues，`m_ci` 为候选 `c` 在 revision
  `i` 的漏检数，使用 `z_i = 100*n*(m_Ai-m_Bi)/D`，其均值即百分点差；
- false finding 与 burden 分别使用
  `z_i=100*(count_Ai-count_Bi)`，均值即每百条 rate 差；
- state agreement 使用每条 0/1 agreement 的差并乘 100；finding Jaccard 使用每条
  Jaccard 差；
- latency／cost 只对相同 sample 和 run number 的有效执行配对，按每 revision 归一后取
  `log(A/B)`，用同一 t 区间并转回相对比值。少于两个有效执行对、非正值或不可观测时，
  该操作轴不可判。

这里的 Wilson 与 paired interval 只是小样本个人选择的描述和决策纪律。Lite 不使用
bootstrap，不做 multiple-comparison 校正，也不作公共 benchmark 或统计认证声明。

### 2.5 practical margins 与结论规则

结果前冻结以下实用界：

| 轴（有利方向） | practical margin |
|---|---:|
| decision-changing miss rate 更低 | **10 个百分点** |
| false findings 更少 | **每 100 条少 10 条** |
| human review actions 更少 | **每 100 条少 10 次** |
| item-state agreement 更高 | **10 个百分点** |
| finding Jaccard 更高 | **0.10** |
| latency 或 cost 更低 | **相对低 20%** |

一个方向只有在点差达到相应界值，且对应 95% paired interval 完全位于该界值的有利一侧
（不跨越 margin boundary）时才是 conclusive。否则按 §2.1 继续下一指标／阶段。区间不可算
也视为不具结论性，而不是零不确定性。

对 3–4 个首次 Dev 有效候选，Top-2 admission 使用同一已冻结轴序，但 stability 尚不可用；
被选入席位的是第三章冻结的 `candidate_slot`／template，而不是只在 Dev bundle 下成立的
`run_config_id`。对每个席位、每个当前指标，先在剩余候选中找点估计最佳者；若多个候选的
最佳点估计精确相同，先按各 slot 映射的首次 Dev `run_config_id` 升序选出唯一 reference，
再只剔除被该 reference 按上述规则 **conclusively** 击败的候选。这个 co-best reference
选择只决定确定性控制流，不表示或报告质量优势。若仍多于一个则继续下一可用指标，所有轴
结束后仍以各 slot 映射的首次 Dev `run_config_id` 升序选择。选定第一席后，从原剩余集合按
完全相同的逐指标规则选第二席。该 ID 只保证 admission 可重复，不能被报告为质量优势。

对 Top-2 的隐藏确认，第一项 conclusive 指标决定方向并停止。若 Primary 没有方向且有预承诺
Extension，按第五章在 pooled 64 上从原始计数重算；不得复用 Primary 区间。所有可用隐藏
确认结束后，终态按以下互斥规则记录：如果每个适用的质量／操作轴的点差都未达到相应界值，
输出 `practically-indistinguishable`；如果至少一个点差达到界值、但没有方向具结论性（区间
跨越界值或不可计算），输出 `inconclusive-uncertain`。两者都不得强迫产生 winner；无有效
比较时仍使用既定的 `no-valid-comparison`，不得把执行失败伪装成不确定性。

## 三、请求配置与观测身份

### 3.1 仅三层身份

Lite 只有三层身份：`bundle_id`、`run_config_id`、`execution_id`。route 是 run configuration
内部字段，不是第四个独立身份。全部 SHA-256 输出为小写十六进制；`JCS(x)` 规范性地表示
**RFC 8785 JSON Canonicalization Scheme** 产生的 UTF-8 bytes。

所有进入 identity、commitment、artifact self-ID 或 inventory digest preimage 的值只能使用
string、boolean、null、integer 或 canonical decimal string；禁止 float、NaN 和 Infinity。
非整数十进制量必须写成不带 `+`／指数／前导零／末尾小数零的十进制 string，且禁止 `-0`。
JCS 输入和输出保留原始 Unicode code point 序列；任何读取、比较、hash 或验证步骤都不得隐式
执行 Unicode normalization。

```text
ordered_sample_identity = sha256(JCS({
  sample_contract_version,
  ordered_revision_ids
}))

bundle_id = sha256(JCS({
  contract_version,
  ordered_sample_identity,
  prompt_sha256,
  result_shape_sha256,
  context_payload_sha256
}))

run_config_id = sha256(JCS({
  bundle_id,
  purpose,
  requested_route,
  requested_provider,
  requested_model,
  requested_execution_parameters
}))

execution_id = sha256(JCS({
  bundle_id,
  run_config_id,
  run_number,
  dispatch_id
}))
```

`contract_version`、精确 prompt bytes 和精确 result-shape bytes 由 `protocol` 拥有；后两者
可以直接内嵌，也可以由 `protocol` 绑定 immutable content-addressed resolver 及预期 hash，
但不得依赖可变路径。对应阶段的 public／protected `sample` instance 拥有精确有序
`revision_id`，以及同序的 source／target／context／公开源码 payload bytes。
`ordered_revision_ids` 是这些 `revision_id` 的冻结数组，`sample_contract_version` 是该 sample
contract 的冻结版本；`ordered_sample_identity` 必须严格按上式计算，空值、排序或版本都不能
由 validator 猜测。`context_payload_sha256` 按 protocol 冻结的唯一 framing 绑定全部精确
payload bytes。

validator 必须从 `protocol` 和对应 `sample` 的所有权字节重新计算三个 component hash 及上述
`bundle_id`，不能信任调用者提交的 hash。每份 `run-manifest` 必须回显
`prompt_sha256`、`result_shape_sha256`、`context_payload_sha256` 和 `bundle_id`；任何 resolver
不可用、字节／顺序／hash 不一致或 bundle 重算不一致都 fail closed。这些所有权和引用不新增
artifact family 或 identity layer。

`purpose` 在未来激活后只能是 `evaluator_selection_v1`。`requested_execution_parameters` 至少
容纳 protocol 要求比较的 reasoning、temperature、max output 等请求值；不得把参数藏在
route 名中。

### 3.2 candidate slot／template 的跨阶段映射

由于 Dev、Primary、Extension 的 bundle 不同，同一候选在各阶段必然有不同的
`run_config_id`。为使 admission 后的候选可机器核对，`protocol` 必须在任何候选输出前：

- 为每个候选冻结一个稳定 ordinal／key 形式的 `candidate_slot`，并绑定恰好一个
  candidate template；slot／template 只是 protocol 内的编排键，明确**不是身份层**，也不
  进入第三个 identity hash；
- 在 template 中冻结唯一一份 canonical requested configuration，其字段恰为 `purpose`、
  `requested_route`、`requested_provider`、`requested_model` 和
  `requested_execution_parameters`；
- 冻结该 slot 到所有适用阶段的 `bundle_id`／`run_config_id` 映射，包括 Dev（repeat 复用同一
  配置 ID）、Primary 和可用时的 Extension。

同一 slot 的 canonical requested configuration bytes 在所有阶段必须精确相等；purpose、
route、provider、model 或任一 execution parameter 都不得漂移。阶段 run configuration 中
只有 `bundle_id` 及由它确定的 `run_config_id` 可以随 bundle 改变。不能满足这种精确相等或
不在冻结映射中的配置，不得被当作已录取候选的后续阶段执行。

### 3.3 requested／observed 分离与 fail-closed

请求值进入 `run_config_id`。实际观测的 provider、model、version 和可观测执行参数只进入
本次 `run-manifest`，**不得**折入或重算 `execution_id`。

`protocol`／run configuration 必须在结果前冻结：

- 哪些身份和执行参数必须可观测，以及每个字段的精确比较规则；
- provider 与 model 始终必需且必须与请求值一致；
- version 只有在结果前明确冻结并对全部候选统一适用时，才允许唯一字面 sentinel
  `unavailable`；不得为个别 route 临时使用；
- 任何意外缺失、额外、不同或无法按冻结规则解析的值都是 mismatch。

只有 requested／observed comparison 全部成功并通过所有 gate，对应 execution assessment 才
可成为 metric-eligible。任一 mismatch 一律标记 `invalid-execution` 并 fail closed；该 assessment
只参与第六章规定的闭合与停止控制，不进入质量指标。不得用“route 大致相同”、显示名称相似
或事后别名映射放行。

## 四、Dev-32

### 4.1 冻结样本与裁决

正好 **3–4 个**预登记候选 requested configuration 直接运行同一冻结 Dev-32，一开始每个
只运行一次。每个候选占用一个预冻结 `candidate_slot`／template，并使用该 slot 映射的 Dev
`run_config_id`。Lite **没有**正式 Challenge dataset、view 或 stage；fail-fast gate 只是
执行资格门，不能改名为 Challenge。

Dev-32 的互斥 primary composition 必须精确为：

| 互斥主层 | 数量 |
|---|---:|
| clean／acceptable | 11 |
| decision-changing defects | 9 |
| terminology／entity-role | 6 |
| context-dependent 或 ordinary substantive | 6 |
| **合计** | **32** |

每条恰好属于一个主层；secondary tags 可以重叠，但不能改变 11+9+6+6 的主计数。Dev 身份、
顺序、精确 source／target/context bytes 和 reference labels 在首个候选输出前冻结。每条 label
必须先由维护者独立完成语义裁决和必要源码核验；候选模型、日常 reviewer 输出或其他模型输出
都不能充当 reference label。

### 4.2 首次执行、Top-2 与重复

- slot 的“第一次 Dev execution”是第一次有持久 dispatch receipt／status 明确证明候选 envelope
  transmission 已接受的 campaign attempt；它在 terminal state 才构造 `run-manifest`。若未通过
  §2.2 correctness／safety gate，立即停止该候选，不给 campaign retry、replacement、repeat 或
  隐藏运行；可终态化的失败执行仍保留并计数。只有持久状态明确证明 non-acceptance 的单次
  pre-transmission Paseo orchestration retry 不算这次 Dev execution；若同一 slot 的初始传输
  尝试及其唯一一次允许重试均被持久状态明确证明 non-acceptance，则整个 campaign 必须无
  `selection-decision` 停止，不得省略该 slot、视为 `invalid-execution`、替换或以更小候选集
  继续，两次尝试均不创建 campaign execution／manifest／assessment 且仅保留在 Paseo
  orchestration 记录中，继续需新授权的 protocol／campaign；`indeterminate-transmission`
  或无法构造有效 terminal manifest 亦使整个 campaign 无 decision 停止；
- 从首次 Dev 有效 slot／template 按 §2.5 的冻结质量／操作顺序选 Top-2；残余 admission tie
  只按各 slot 映射的 Dev `run_config_id` 决定，不声称质量更优；
- **仅 Top-2 slot／template** 在完全相同、同序、同字节的 Dev-32 上获得第二次 execution，
  用于 §2.3 stability；第二次复用对应 Dev `run_config_id`，但使用新的 `run_number`、fresh
  `dispatch_id` 和 `execution_id`；
- 首次有效 slot 少于两个时，记录 `no-eligible-pair` 并停止；不得按结果引入新候选、递补
  已失败候选或更换 Dev 条目；
- Top-2 repeat 任一无效时记录 `no-valid-comparison`，不进入隐藏确认。

## 五、Primary / Extension

### 5.1 隐藏身份与 commitment

在**任何候选输出之前**冻结精确有序 Primary-32 IDs；若 frame 为目标 96 模式，同时冻结
精确有序 Extension-32 IDs。Dev、Primary、Extension 不得重叠，所有身份都绑定冻结时的当前
revision bytes。

版本控制可见工件只跟踪一个加盐的 `holdout_commitment_sha256`，以及必要的 `frame_mode`／
`extension_available` 状态。其唯一计算式为：

```text
holdout_commitment_sha256 = sha256(
  nonce_raw_32_bytes || 0x00 || JCS({
    contract_version,
    primary: [{revision_id, payload_sha256}, ...],
    extension: [{revision_id, payload_sha256}, ...]
  })
)
```

`nonce_raw_32_bytes` 必须恰为 32 个随机原始 bytes；外部保存时编码为 base64url，但进入 hash
之前必须先解码，`0x00` 是单个分隔 byte。`primary` 与 `extension` 数组分别按冻结 sample 顺序，
每项的 `payload_sha256` 绑定该 revision 按 protocol framing 得到的精确 payload bytes；
`extension_available=false` 时 `extension` 必须是 `[]`，不能省略。contract version、任一数组
身份／顺序／payload hash 或 nonce 的变化都产生新 commitment，不能原地解释旧值。

上述 JCS preimage、精确 IDs、顺序、payload、nonce、labels、findings 和 adjudication 全部留在
ignored／local protected `sample` instance／master asset，绝不进入版本控制；公开的 digest
本身不暴露这些 IDs。它们必须按 §7.1 对 candidate reviewer 不可读，只有 ORCHESTRATOR／
dispatch builder 可以读取；授权执行只把当前阶段允许的有界投影冻结进 candidate envelope，
不把 protected instance 变成可读资产。

### 5.2 延迟裁决与 reveal

Primary 可在 Top-2 已知后、但必须在 Primary evaluator execution **之前**完成维护者语义裁决
和源码核验。这里是对 selection reference 的独立确认；池中的日常译文裁决只提供候选证据。
裁决者不得查看这批条目的任何候选输出。最终裁决若使预期 strata 与 frame 初筛不同，只如实
报告 realized strata；不得重抽、替换或跨层补齐。

流程固定为：

1. 两个 Top-2 slot／template 都使用各自预冻结映射的 Primary `run_config_id`，在完全相同的
   Primary-32 上各运行一次；
2. 若 §2.5 产生 conclusive direction，立即停止，Extension 不运行；
3. 若无方向且 `extension_available=true`，先在不查看 Extension 候选输出的条件下完成其
   维护者裁决，再让两个 Top-2 使用各自映射的 Extension `run_config_id` 运行 Extension-32；
4. 在 **Primary+Extension 64** 的原始计数上从头计算同一决策规则；
5. Extension 单独永远不能产生结论；隐藏确认耗尽后，所有适用点差均低于界值才输出
   `practically-indistinguishable`；存在达到界值但区间跨界或不可计算的点差时输出
   `inconclusive-uncertain`。

`extension_available=false`、Primary/Extension 身份、顺序或 adjudication 时序都不能因
Primary 结果改变。无效执行不能触发补样、替换或隐藏扩容。

## 六、四类最小工件

### 6.1 恰好四类未来 machine contract family

任何未来实现只定义以下 **四类** machine contract family：

1. **`protocol`**：不可变的结果前 campaign policy，包含候选 slot／template、唯一 canonical
   requested configuration、所有适用阶段的 `bundle_id`／`run_config_id` 映射、精确 prompt／
   result-shape bytes（或绑定预期 hash 的 immutable content-addressed resolvers）、确定性的
   execution ordering／admission／stopping recipe、决策顺序与 margins、identity observability、
   frame mode，并明确绑定版本控制可见的 public `sample_id` 和同一 sample 中的
   `holdout_commitment_sha256`，以及失败语义、成本门和授权边界；
2. **`sample`**：每个 public／protected stage instance 拥有该阶段的精确有序身份，以及同序的
   source／target／context／公开源码 payload bytes。public instance 还持有 Dev 内容和版本控制
   可见的 Primary／Extension commitments；同一 family 的 protected instance 在本地持有精确
   隐藏内容，永不进入版本控制且 candidate reviewer 不可读；不得另立 holdout contract；
3. **`assessment`**：不可变的宿主所有 assessment family；用下述 discriminator 区分有效执行、
   无效执行与最终 selection decision，并按各 variant 绑定 raw output、manifest、执行证据或
   决策输入；不得为失败结果或最终报告建立第五类 contract；
4. **`run-manifest`**：每次有持久 receipt／status 证明已接受的 campaign execution 最终必须有
   恰好一份不可变 terminal manifest。它只能在执行达到 terminal state 后，由绑定 `dispatch_id`、
   acceptance state／time 的持久 receipt 与可核验 terminal evidence 构造，并绑定
   `protocol_id`、applicable stage sample identity、requested configuration、observed identity、
   `bundle_id`／`run_config_id`／`execution_id`、`run_number`／`dispatch_id`、
   `prompt_sha256`／`result_shape_sha256`／`context_payload_sha256`、terminal timestamps、
   cost／latency、failure class 和全部 gate 结果。执行中的瞬态 orchestration state 不是 Lite
   artifact；持久状态证明未接受的 pre-transmission retry（含同一 slot 的初始尝试及其唯一
   一次允许重试均被明确证明未接受的情形）不创建 manifest／assessment，仍仅保留在 Paseo
   orchestration 记录中，且该双重未接受情形使 campaign 无 `selection-decision` 停止，不得
   省略、视为无效执行或以更小候选集继续。accepted 后 incomplete
   或 crash 也必须在证据允许时终态化为失败 manifest 和对应的保留 invalid assessment；无法构造
   有效 terminal manifest 时，campaign 无 decision 失败。

每个未来 campaign 只使用一个由宿主拥有、append-only、ignored 的 campaign directory／
namespace，以精确 `protocol_id` 为 key。该 namespace 必须容纳该 campaign 的**全部** terminal
`run-manifest` 和全部 `valid-execution`／`invalid-execution` assessment；最终
`selection-decision` 也是同一个 `assessment` family 的终态对象。这个目录边界只是四类工件的
闭合规则，不是 generic registry、第五类 contract 或新的 identity。

`assessment` family 只使用一个 `assessment_kind` discriminator，且只允许三个互斥值。对两个
execution variant，`structurally_valid`、`control_flow_required` 与 `metric_eligible` 是三个
相互独立的必填 boolean：结构有效只说明 assessment 本身通过 exact-field、引用与 self-ID 校验，
不代表 execution 通过 gate；控制流必需表示它必须进入 namespace closure 和 stopping replay；
metric eligible 才表示它可以进入质量指标。

- `valid-execution`：绑定捕获的 raw output bytes 及其 hash、`protocol_id`、applicable stage
  sample identity、`run_manifest_id`、完整有序的 per-revision state／findings、evidence
  validation 和 host matching；只有 requested／observed 比较及全部 gate 成功后才能使用该
  discriminator，并必须记录 `structurally_valid=true`、`control_flow_required=true`、
  `metric_eligible=true`；
- `invalid-execution`：绑定捕获的 raw output bytes 及其 hash（零字节输出也必须显式记录为空
  输出并计算 hash）、`protocol_id`、applicable stage sample identity、`run_manifest_id`、
  failure class，以及可选的 partial-parse diagnostics。一份 well-formed invalid assessment 必须
  记录 `structurally_valid=true`、`control_flow_required=true`、`metric_eligible=false`；它会被
  闭合与停止控制消费，但永远不进入质量指标，也不要求或允许伪造完整有序 per-revision items，
  局部解析内容只能是诊断信息；
- `selection-decision`：绑定 `protocol_id`、全部 campaign execution assessment 的精确有序
  closure（有序 `input_assessment_ids` 及每项对应的 `execution_id`／`run_number` campaign
  attempt）、public `sample_id`、`holdout_commitment_sha256`、本次 look 所适用的 stage sample
  identity chain、原始计数、区间、outcome、下述完整 execution artifact inventory 及其 digest，
  并以 `namespace_closed=true` 标记 namespace 闭合。outcome 必须能明确记录
  `practically-indistinguishable`、`inconclusive-uncertain` 及既定的 gate／eligibility 终态，
  而不能把不确定终态写成 winner。

该有序 closure 不是调用者可挑选的输入列表。validator 必须从冻结 `protocol` 的 execution
ordering、admission 和 stopping recipe、完整 manifests 以及按序在先且
`control_flow_required=true` 的 valid／invalid assessments 确定性重放，推导截至合法停止点所
要求的全部 campaign execution assessment／attempt 顺序。任何有持久 acceptance 证明后产生的
无效 execution 都必须进入该 closure 并触发既定停止；只有持久状态证明未接受、只记在 Paseo
orchestration 的 pre-transmission retry（含同一 slot 初始尝试与单次允许重试均被明确证明
未接受且 campaign 已无 `selection-decision` 停止的情形，两次尝试均不进入）不进入。

到达合法停止点时，宿主必须先完整枚举该 `protocol_id` namespace 中所有 pre-decision execution
artifact。`execution_artifact_inventory` 必须包含每一份 terminal `run-manifest` 和每一份
valid／invalid execution assessment 的 `{artifact_family, artifact_id, artifact_sha256}`；其中
`artifact_sha256` 是包含 self-ID 字段的完整 artifact JCS bytes 的 SHA-256。inventory 按
`artifact_family`、再按 `artifact_id` 的 UTF-8 byte lexical order 排序，且
`execution_artifact_inventory_sha256 = sha256(JCS(execution_artifact_inventory))`。随后构造并
写入嵌有该 inventory／digest 的 `selection-decision`，由其 `namespace_closed=true` 关闭
namespace；`selection-decision` 自身明确排除在 inventory 之外，以避免 self-reference，且
不得另建 closure marker 或 registry。

validator 必须能完整枚举已闭合的 namespace，并将实际全部 pre-decision execution artifacts
与 decision 内 inventory 逐项 exact-match 后重算 digest；缺失、额外、重复、hash／identity
不一致、decision 后新增或在 stopping recipe 已要求停止后创建的 artifact，以及 namespace
访问不完整或无法证明完整，均使 `selection-decision` fail closed。其有序 assessment closure
还必须与 inventory 中的 execution assessments 精确对应，不能靠排序 inventory 隐藏重排或
选择性排除。同一 slot 的初始传输尝试与单次允许重试均被持久状态明确证明未接受、
`indeterminate-transmission`、已接受 execution 无法重建有效 terminal manifest，
或其他无法完成该闭合的情况都使 campaign 无 selection decision 失败；前者两次尝试均不进入四类工件且不得以省略、视为无效执行或更小候选集继续。

applicable stage sample identity 至少包含 stage、该阶段对应的 public／protected `sample_id` 和
精确有序 sample identity；Primary／Extension 还必须带回 public sample 中同一个
`holdout_commitment_sha256`。每份 `run-manifest` 的这些字段必须与其 `protocol`、`sample` 和
bundle 精确一致；`valid-execution` 与 `invalid-execution` assessment 中的同名字段及
`run_manifest_id` 又必须与所引用 manifest 精确一致，否则 assessment 本身验证失败。最终
`selection-decision` 必须拒绝输入 assessment 间混合 `protocol_id`，也必须拒绝 public
`sample_id`、holdout commitment 或适用 stage sample identity chain 的任何混用／断裂。

validator 必须解析 `protocol` 所有的精确 prompt／result-shape bytes（或其不可变 resolver），
并从对应 public／protected `sample` 取得精确有序身份和 payload bytes，重新计算
`prompt_sha256`、`result_shape_sha256`、`context_payload_sha256` 及第三章的 `bundle_id`。
重算值必须与 protocol mapping、manifest 回显和 assessment 引用全部精确相等；resolver、字节、
顺序或引用有任何不可验证之处都 fail closed。

为避免 `protocol`↔`sample` self-ID 循环，先独立计算 public `sample_id`，其 sample 对象不要求
也不得为了这条绑定而纳入 `protocol_id`；随后 protocol 按精确值引用该 public `sample_id` 与
`holdout_commitment_sha256`。上述 byte ownership、resolver 和 closure 都只是四类工件之间的
内容或引用，不新增 contract family 或第三章以外的执行身份层。

捕获的原始返回 bytes 在 `assessment` 内以可逆形式保留并绑定 hash；显式空输出不是字段缺失。
它不形成独立 `result` contract；人类可读展示也只是 assessment 的渲染，不形成独立
`report` contract。

四类工件规范性地统一使用第三章定义的 RFC 8785 JCS UTF-8 bytes；不得用“排序键且去空白”的
近似实现替代。所有进入 self-ID 的值都遵守第三章的类型、canonical decimal string 和 Unicode
code point 规则。验证必须 exact-field、拒绝未知字段并 fail closed。每类使用自己的 self-ID
字段（`protocol_id`、`sample_id`、`assessment_id`、`run_manifest_id`）；计算 self-ID 时只省略
该 self-ID 字段，对剩余完整对象取 `sha256(JCS(object_without_self_id))`，不能省略其他字段。

本文件没有创建 schema、实例、validator、代码或测试；它们只有在独立授权的实现任务中才
可以存在。

### 6.2 用户批准的局部回收矩阵

| 处置 | pre-Lite full implementation 中的内容 | Lite 规则 |
|---|---|---|
| **仅回收概念** | RFC 8785 JCS／SHA identity；exact-field／fail-closed validation；requested／observed separation；evidence／coverage checks；no-input-mutation tests；与 Gold／Silver／TM 的 result isolation | 只采纳设计思想；不得把旧 contract ID、schema、代码或测试视为 Lite 实现 |
| **使用全新 Lite contract ID 重设计** | model result 折入 host assessment；三层 identity；Dev／Primary／Extension 尺寸；decision assessment；protected sample representation | 未来从空白的 Lite family 设计，不复制旧身份或把旧文件改名升级 |
| **不得原样复用** | 320→160 protocol、Challenge、S0–S10、dual preregistration、commitment lifecycle、paired bootstrap、standalone result／report contracts、现有八份 full schemas、完整 validator 或完整 test suite | 全部保持延期完整协议语义，不得悄然成为 Lite 依赖或验收门 |

任务开始前的 pre-Lite 文件继续是 **non-normative**。本 Task B 不编辑、不删除、不采用它们；
其去留等待单独的 hash-preserving archive／cleanup 任务。未来实现必须先按独立决策归档原件，
再创建 fresh Lite assets；不得通过修改或重命名旧文件把它们变成 Lite authority。

> 后续裁定（2026-08-17）：该独立任务已执行，结论为**全部丢弃**，精确身份（路径／行数／
> SHA-256）记录于
> [`evaluator-selection-full-impl-discard-manifest.md`](evaluator-selection-full-impl-discard-manifest.md)。
> 因此工作树中已不存在可复用的 pre-Lite 文件，本节的"不得原样复用"约束继续对任何未来重建生效。

## 七、Paseo 边界

### 7.1 唯一未来执行路径

未来若另行激活，候选执行必须同时满足：

- `role=reviewer`、`purpose=evaluator_selection_v1`；
- 每次 fresh session／dispatch、同一 workspace、已验证 current ORCHESTRATOR parent lineage；
- reviewer read-only guard、候选 identity、bounded envelope 和精确有序 coverage；
- candidate reviewer 的 read allowlist 只包含本次冻结的 candidate envelope、result-shape bytes，
  以及 envelope 逐项明确引用的公开源码路径；不得授予 workspace-wide read；
- envelope 只含本次任务允许的有界 revision、必要上下文和明确引用的公开源码证据；
- 每次返回都按第三、六章由宿主 fail closed 验证。

protected Primary／Extension master assets 中的精确 IDs、顺序、payload、nonce、labels、
adjudication／findings，以及所有其他 stage bundle，都必须位于该 reviewer 可读 allowlist 之外，
并通过物理分离或权限分离保证不可读。只有 ORCHESTRATOR／dispatch builder 可以读取这些
master assets；builder 在对应隐藏阶段获授权后，只把当前阶段执行所需的有界 revision identity
和 source／target／context 投影进冻结 envelope，绝不投影 reference labels、adjudication、
findings、nonce 或其他 bundle。

每次 dispatch 都必须在 outbound transmission 前验证 read allowlist 和上述 deny isolation；
无法验证就 fail closed，且不得发送 envelope。同一 workspace 与 read-only guard 本身只说明
workspace／写权限边界，**不能**证明隐藏数据的读隔离。

禁止 direct-provider 调用，也禁止恢复 retired blind runner 或任何等价 fallback。未来本地工具
可以构建、hash、校验和比较四类 artifact，但永远不能执行候选模型。Paseo 不可用或身份／
lineage 无法验证时只能停止，不能切换 runner。

### 7.2 模型最小输出与宿主权限

模型对每条 revision 的最小输出为：

```text
revision_id
assessment_state
context_sufficient
findings[] {
  error_family
  phenomenon
  meaning_change
  source_evidence
  target_evidence
  explanation
}
```

`clean` 只表示该条是有效 assessed item 且 `findings=[]`。`context-insufficient` 与
`source-issue` 必须是显式 state，不能当作 clean，也不能用空 findings 掩盖。

模型不得分配 severity，不得决定 Gold／Silver、reuse／TM eligibility、最终 score、winner
或生产映射。只有宿主／维护者可以在另有授权时派生这些值；selection outcome 本身仍不授予
上述权限。

### 7.3 inactive 边界

本 SPEC **不激活** `evaluator_selection_v1`。未来激活至少需要独立修改并审核
`AGENTS.md`、角色定义、Paseo 契约和相关 gate；该 infrastructure diff 必须由独立 Paseo
REVIEWER 与 SENIOR_REVIEWER 从同一 SPEC／diff 交叉复审。完成本文件不能自动启动该实现
任务、外部传输或 campaign。

## 八、人工构造／真实证据分离

每个 evidence pool／sample 条目必须恰好标记一个 evidence class：

- **`real-adjudicated`**：真实小批次自然 revision，已由维护者裁决并有适用的源码核验引用；
- **`controlled-artificial`**：为已知现象人工构造或控制变化的案例；
- **`fake-replay`**：用于离线重放的伪输出／伪输入。

只有 `real-adjudicated` 的自然 revision 可以进入 Dev／Primary／Extension，并支持生产 evaluator
选择。`controlled-artificial` 只能作为诊断或 execution-gate 证据，必须单独报告；它不能修补
缺失的真实主层、提高最终证据权限或混入 production-selection 指标。

`fake-replay` 永远标记 `non-evidentiary-offline-replay`，只允许测试 parser／validator。它既不
能证明候选质量，也不能消费、模拟或替代真实 campaign 结论。三类数据的计数、结果和展示
不得合并。

## 九、成本闸门

Lite 的主成本不是四类 contract 或本地校验代码，而是 **Dev-32 的独立维护者语义裁决与必要
源码核验**。即使证据池来自日常译文批次的已裁决副产品，选择 reference label 的隔离确认仍需真实人工
时间。

因此，未来可以实现四类 contract 和 Paseo purpose 后继续停在 campaign 之前；实现完成不
产生运行义务。只有以下条件全部满足，campaign 才能开始：

1. 维护者明确接受 Dev-32 的人工成本；
2. evidence pool 有足够 eligible `real-adjudicated` revision 支持冻结组成；
3. 候选 bundle 的外部传输已按 role、purpose 和内容范围明确授权；
4. 冻结的 protocol／sample 已完成独立复审。

若 evaluator 选择的边际价值低于直接修复译文，应回到译文改进，而不是为了沉没成本
继续选型。Primary／Extension 的后续人工投入同样受这一原则约束，但不能在看到结果后改写
已冻结的样本或规则。

## 十、升级条件

延期完整协议只有在以下 **至少一项**发生时才可以被提出激活：

1. 需要公开发布 comparative benchmark；
2. evaluator 输出将自动获得 Gold／Silver／TM authority；
3. Lite 无法区分 production candidates，且该区分在操作上确有重要意义；
4. 多名独立 maintainer／annotator 需要更强的实验治理；
5. evaluator findings 可以在没有 mandatory human review 的情况下触发自动修改译文。

满足条件只允许提出新的 infrastructure 决策，并不自动授权完整协议。实际激活仍需另行确定
范围、授权、实现和交叉审核；它必须创建自己的新工件，不能修改、扩写或重新解释既有 Lite
artifact。

## 参考与符合性

本规范的边界与以下当前文档一致：

- [`AGENTS.md`](../../AGENTS.md)：Paseo、外发和基础设施审核总规则；
- [`evaluator-selection-full-impl-discard-manifest.md`](./evaluator-selection-full-impl-discard-manifest.md)：
  pre-Lite 全量实现资产的最终处置记录；
- [`translation-quality-evaluator-selection-v1.md`](./translation-quality-evaluator-selection-v1.md)：
  `design-reference / full protocol deferred`；
- [`project-roadmap.md`](../../docs/project-roadmap.md)：Lite 渐进证据所挂接的日常译文主线；
- [`paseo-orchestration-v2-contract.md`](../../docs/paseo-orchestration-v2-contract.md) 与
  [`paseo-translation-context-review-v1-contract.md`](../../docs/paseo-translation-context-review-v1-contract.md)：
  当前 Paseo／语境审核边界；
- [`i18n/quality/README.md`](../../README.md)：现有质量资产及 deferred 状态。

本文不修改或重解释上述契约，不声称解决 v3 calibration、official-120、M5／M6、
Gold／Silver／TM 或 production mapping。所有未来实例都必须以冻结 protocol 为准，保留失败，
并遵守“无结果触发替换、放宽或扩样”的 fail-closed 边界。
