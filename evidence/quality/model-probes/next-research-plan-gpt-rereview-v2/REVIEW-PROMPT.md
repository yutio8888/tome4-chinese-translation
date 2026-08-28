# 独立二次方法复审

请把随附方案当作一份新的修订候选，而不是默认成功的整改结果。你的任务是判断它是否已经足够明确，可以开始冻结第一阶段；同时识别会使后续阶段不可识别、不可执行或可被事后解释的剩余问题。

重点检查：

1. Phase 0 是否真正把 estimand、单位、分母、missingness、reserve 和 stopping rule 转化为可机械核验的冻结合同。
2. Phase 1 的 36 个独立 items、A/B arms、context extractor、FINDING/UNCERTAIN 计分、route-equal 汇总和数值门槛是否内部一致；尤其检查伪重复、control 定义、泄漏、离散门槛和 mixed-result 处理。
3. Phase 2 的目标总体、PPS 两阶段抽样、纳入概率、权重、盲化源码审计、unknown provenance、indeterminate/unreachable 上下界能否实际重建；区分可行性 pilot 和总体率估计。
4. Phase 3 是否只估计其声明的 reviewer × generator-output 操作性交互；检查 complete-block selection、两个 generation outputs 的 mutant/control 分配、主要 risk difference、聚类单位、control guardrail 和可估计性。
5. 跨阶段预算门槛是否被误写成科学前提，任一 gate 是否依赖未定义量，停止规则是否允许隐性追样或换指标。
6. 只把会阻止相应阶段有效推断的问题列为 fatal；能够在冻结前明确补充的列为 major。不要因措辞不完美夸大 severity。
7. 若认为第一阶段已经可以进入冻结准备，明确列出冻结前仍必须机械化的清单；若不能，给出最小必要修订，不得重写整套研究计划。

限制：

- 只能依据本 prompt、`PLAN-UNDER-REVIEW.md` 和输出 schema。
- 不使用网络或外部知识，不读取任何上一轮审阅、综合、结果或其他项目文件。
- 当前没有独立母语人工审核者；结论限于固定源码可裁决的客观机制。
- 不得建议追加既有八条实验的 Run D。
- 不得把重复 run、route、arm 或 generation observation 当作新的独立 source items。
- 数值门槛可以是 materiality/budget rules，但不得伪称功效或显著性阈值。
- 输出一个严格符合 schema 的 JSON 对象，不得包含 Markdown fence 或额外说明。
