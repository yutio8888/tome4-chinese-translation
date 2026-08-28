# 下一步研究方案 v1

状态：经独立 GPT-5.6 Sol high 方法审阅后，本地主代理批判性综合。

日期：2026-08-27

## 研究顺序

1. 统一预注册与可识别性检查。
2. 精简的 runtime source-context pilot。
3. 前瞻性自然残余审计。
4. 只有通过预算优先级与 provenance 门槛时，才做 reviewer × generator-output pilot。

现有八条 UI/日志设计不再追加 Run D。第三阶段研究的 estimand 明确降格为“匿名 generator outputs 上的操作性 reviewer × origin interaction”，不得直接称为同族偏差或心理偏好。

## 阶段 0：统一预注册与可识别性检查

模型调用：0。

每个后续实验在任何推理前必须冻结：

- 唯一主要 estimand 和一个主要 contrast；
- 抽样单位、目标总体、排除规则、纳入概率、随机种子和 ordered reserve；
- clean 判据、mutation map、上下文提取规则和缺失处理；
- 路线、CLI 版本、模型、effort、输入顺序、prompt、schema 和计分器；
- UNCERTAIN、indeterminate、unreachable 的计分与分母规则；
- 数值 go/no-go 门槛、mixed-result 动作和停止规则；
- verifier 所需的输入、匿名映射、arm 差异及 reserve 顺序哈希。

任一主要 estimand、分母、上下文规则或结果无关的缺失处理仍不明确，则 no-go，不运行模型。重复 run 是同一 item 的重复测量，不增加独立样本量。

## 阶段 1：Runtime source-context pilot

建议目录：runtime-source-context-pilot-v1/。

### 问题

固定、机械提取的源码上下文是否能提高需要运行时证据的客观缺陷检出，同时不增加 source-refuted control 候选？

### 样本

冻结 36 个互不重复的 source items，每个 item 只出现一个 target variant：

- 12 个 runtime_source_required 注入变异；
- 12 个同类、推理前完整源码核验的 clean controls；
- 6 个 surface_bilingual 注入变异；
- 6 个同类 clean controls，作为预注册负对照。

确定性 lint_detectable 项不进入模型主要实验，另由 lint 工具报告覆盖率。样本不得包含同一 source item 的 control/mutant 近重复对，以免 reviewer 通过配对猜标签。

### Context 构造

在 mutation assignment 和 sealed reference 揭示前冻结机械提取器：

1. 由已冻结 manifest/source tag 定位定义；
2. 只提取包含目标定义的源码块，并至多追加一个直接调用定义；
3. 使用固定字符上限和确定性截断；
4. 只保留脱敏原始代码，不写自然语言 expected claim；
5. 失败统一输出 CONTEXT_MISSING，不得逐条人工补片段；
6. 对绝对路径、mutation label、reference 词汇和人工结论做拒绝式泄漏检查。

A 臂为 source/target；B 臂只额外增加上述 source_context。除此字段外，ID、顺序、prompt、schema 和计分完全一致。

### 运行与指标

- 4 routes × 2 arms × 2 byte-identical runs = 16 次 reviewer 调用；
- 每个 arm 的两次运行字节完全一致；完成两次后停止；
- 主要 contrast：每个 run 中，四路线等权的 runtime-mutant 配对 recall 差 B - A；
- 正确原子主张的 FINDING 或 UNCERTAIN 计主要 detection；FINDING-only 单列；
- 主要 false-positive guardrail：source-refuted runtime-control candidate rate 的 B - A；
- surface 项、逐路线结果、成本、token 和翻转为次要描述，不参与改换主要结论；
- item 是推断和聚类单位，route 是固定比较对象，run 只是重复测量。

### 决策门槛

只有同时满足以下条件，后续实验才统一采用 B：

- 两个 frozen runs 的等权 runtime recall 增量均至少为 0.20；
- 每个 run 至少 3/4 routes 的增量为正；
- 每个 run 的等权 source-refuted control candidate-rate 增量不超过 0.05；
- 任一路线、任一 run 最多新增一个 source-refuted control 候选；
- 没有出现经源码确认的 control 污染。

这些数值是预算与输入契约的 materiality rules，不是功效或显著性结论。失败、mixed 或边界结果一律保持 A 作为后续默认输入，报告探索性逐路线结果但不增加第三次运行。

## 阶段 2：前瞻性自然残余审计

建议目录：prospective-residual-audit-v2/。

### 目标总体与抽样

在固定生产 commit 和 provenance snapshot 上冻结公开源码组件中的 eligible terminal contextual revisions。采用两阶段、可重建的概率抽样：

1. 在 same-family-only、cross/mixed-family 和 unknown provenance 层内按 eligible revision 数量对 task 做 PPS 抽样；
2. 每个入选 task 用冻结 seed 等概率选择一个 terminal revision；
3. 记录每个 revision 的总纳入概率和层权重；
4. 排除既有实验、prompt 开发集和历史条目级 reference，但不因 source 难以核验而事后替换；
5. 冻结 40 个独立 task/revision 单元作为可行性 pilot。

该 n 只能检验可行性和给出宽区间；若未来要求指定精度，必须在新实验冻结前按区间宽度目标重新设计样本量。

### 裁决顺序

1. 在任何 reviewer 输出揭示前，按统一模板完成全部 40 条固定源码审计并锁定证据；
2. 裁决者不知道模型提名和路线，但如实记录其不是独立人工审核者；
3. 所有条目使用相同审计深度和证据充分性规则；
4. verdict 为 confirmed、refuted、indeterminate 或 unreachable；
5. reference 锁定后，四路线各做一次匿名独立审核，共 4 次模型调用，再揭封计分。

### 分母与报告

- 使用纳入概率权重报告 confirmed 下界；
- 同时报告把 indeterminate + unreachable 全计为缺陷的上界；
- 只有 determinate 比例至少 90% 时才附加单一点估计；
- 只有 provenance 可分类比例至少 90% 时才报告流程分层描述；
- unknown provenance 永不静默排除；
- same/cross-family 差异只作描述，不能作因果归因；
- 模型 recall 和候选效率是 reference 锁定后的次要结果，不参与自然残余率分母。

### Go/no-go

任何结果依赖替换、抽样权重不可重建或统一审计模板失效，均停止总体率推断，只保留逐条事实和识别区间。

若至少 4 个 confirmed residuals 分布在至少 4 个独立 task，且 determinate 与 provenance 门槛均通过，则 origin pilot 获得预算优先级；否则暂缓。这个门槛只决定预算，不是 origin interaction 可识别性的科学前提，也不证明不存在 reviewer-origin 作用。

## 阶段 3：条件启动的 Reviewer × Generator-output pilot

建议目录：reviewer-generator-output-pilot-v1/。

### Estimand

主要 estimand 是 GPT reviewer 在匿名 GPT-origin mutant outputs 与匿名 non-GPT-origin mutant outputs 上的绝对检出率差。它是特定模型、prompt 和 clean-block 总体上的操作性交互，不能称为已识别的同族偏差。

### 生成与 clean blocks

1. 冻结 16 个 ordered source items，其中目标为前 12 个完整块，后 4 个为预注册 reserve；
2. 四个 generator origins 各用两个独立 ephemeral generation runs 生成全部 16 项，共 8 个批量生成调用；
3. 在 reviewer 推理前，对 128 个 baseline outputs 做完整源码核验；
4. 一个 item 只有在 4 origins × 2 generation replicates 全部 clean、同一 mutation template 对全部输出可适用时，才构成完整块；
5. 按冻结顺序选择前 12 个完整块；不足 12 个则 no-go，不修文、不动态补生成；
6. 按 origin 报告生成失败、天然缺陷、template 不可用和 reserve 使用，estimand 明确限于完整 clean blocks。

### Mutation 分配与 reviewer 运行

- 对每个 item × origin 的两个 independent generations，按冻结平衡表随机指定一个 mutant、一个 control；
- mutation 类型、位置和 generation-label assignment 跨 item/origin 平衡；
- 形成 12 × 4 × 2 = 96 个 variants；
- 四 reviewers 审核同一个匿名、冻结顺序和 schema 的列表两次，共 8 次 reviewer 调用；
- 第二次后停止，不增加新 generation 或第三次 reviewer run。

两个 generation outputs 用于降低单一输出绑定和进行区组随机化；由于每个 replicate 只承担 mutant 或 control，不能把“两个 generation replicates 分别同方向”作为独立 gate。分析中将 generation assignment 作为重复测量/区组因素，而不是伪造 replicate-specific interaction。

### 分析与门槛

- 主要 contrast 仅为 GPT reviewer 的 GPT-origin 与 pooled non-GPT-origin mutant risk difference；
- 以 source item 聚类，控制 mutation 类别、位置和 generation assignment；
- 完整 4 × 4 reviewer-origin 矩阵、其他 reviewers 和 FINDING-only 均为次要描述；
- 两个 reviewer runs 的主要 contrast 必须同方向且绝对差均至少 0.15；
- leave-one-item-out 后不得反向；
- own-origin 与 non-own-origin 的 control candidate-rate 绝对差不得超过 0.10；
- 任何通过结果只称为“值得 fresh holdout 验证的操作性交互信号”，不得称为同族偏差；
- 未通过、mixed 或边界结果统一为证据不足，停止且不追样。

## 统一停止规则

- 不追加现有八条设计的 Run D；
- 每个实验达到冻结 item 数和 run 数即停止；
- harness/网络/解析错误不计模型成绩；有成功 envelope 时只修解析并复用；
- 不因结果接近门槛增加样本、run、指标或 reserve；
- 任何无法重建的抽样框、匿名映射、arm 差异、generation assignment 或权重都阻止相应总体推断；
- 主观语言质量继续标为需要外部独立审核，不补写客观 ground truth。
