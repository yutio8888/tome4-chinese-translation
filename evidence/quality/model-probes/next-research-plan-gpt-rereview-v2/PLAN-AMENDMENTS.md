# 二次复审后的约束性补充

状态：本文件是 `next-research-plan-gpt-review-v1/PLAN-REVISED.md` 的约束性补充，不替代其研究顺序。

日期：2026-08-27

## 范围校正

上一版是研究路线图，不是 `runtime-source-context-pilot-v1` 的已冻结执行包。二次复审没有发现致命设计问题，但确认 Phase 1 尚不能直接推理。下一步只能进行零模型调用的合同编写与 preflight；只有下列约束全部被 schema 和 verifier 机械证明后，才能建立 Phase 1 推理冻结点。

## Phase 0 的最低可执行合同

每个阶段必须另建版本化目录，并在推理前提交：

- 规范化 `EXPERIMENT.json` 和 JSON Schema，枚举 estimand、有限/超总体范围、item/claim/variant/task 单位、arm、route、run、missingness、reserve、排除和停止状态；
- 唯一有序 manifest、reference/atom-map 哈希、prompt、输出 schema、scorer、gate 公式和全部输入哈希；
- 只读 preflight verifier，机械检查 item 唯一性、类别数量、顺序、arm 唯一差异、context 状态、匿名映射、reference 隔离、分母、reserve 顺序和交叉字段约束；
- 成功 fixture 与至少覆盖缺项、重复 item、arm 漂移、reference 泄漏、边界等号、reserve 越界和哈希漂移的失败 fixtures；
- verifier 非零退出即 no-go，不能用人工声明覆盖。

“byte-identical runs”只表示请求 payload、顺序、模型参数和 schema 完全相同，不要求响应字节相同。四条 route 是固定比较对象，run 是重复测量。

## Phase 1 的绑定修订

### 有限总体与选择记录

主要 estimand 限于本实验冻结的 12 个 `runtime_source_required` mutant items，不外推到未定义的源码总体。12 个 runtime controls、6 个 surface mutants 和 6 个 surface controls 只服务于 guardrail 或负对照。

Phase 1 manifest 必须保存候选框快照、有序选择规则、全部排除及原因。任何人工难度判断必须在 reviewer 输出前完成并留痕；不得因结果替换 item。若未来需要总体外推，必须另建概率抽样实验。

### Context missingness

最终冻结的 36 个 items 必须全部由机械 extractor 产生有效 B-arm context。任一 `CONTEXT_MISSING` 都使 preflight 失败并阻止模型调用；不得在同一版本中逐条排除、替换或让缺失标记进入主要分母。修复 extractor 或更换样本必须另建冻结版本并保留失败版本。

A/B 唯一允许差异是 B 中新增的 `source_context` 字段；verifier 必须重建并逐字节比较其他字段。

### 原子主张与 item-level 计分

在推理前冻结 sealed atom map 和 scorer fixture。对每个 mutant item、arm `a`、route `r`、run `t` 定义：

- `D[a,r,t,i]=1`：至少一条 `FINDING` 或 `UNCERTAIN` 候选准确指向该 item 的 sealed objective atom；仅主题相关、部分主张但未识别原子机制或错误主体均为 0；
- `F[a,r,t,i]=1`：同上，但匹配候选标签必须是 `FINDING`；
- 重复匹配只折叠为一次 item detection；额外错误主张不取消正确 detection，但另计 refuted claims；
- 对 clean control 定义 `C[a,r,t,j]=1`：至少出现一条可由固定源码裁决的客观机制 `FINDING` 或 `UNCERTAIN` 候选；同一 item 多候选折叠为 1；
- `source-refuted candidate` 是 `C=1` 且全部对应客观主张经冻结源码证据驳回；主观语言意见不进入 `C`。

若推理后发现任一 frozen clean control 实际存在客观污染，本版本不得作 adopt-B 总体裁决，也不得替换后重算；只保留逐条事实并另建版本。

### 主要公式与精确门槛

对每个 run 分开计算：

- `R[a,t] = (1/48) * sum_r sum_i D[a,r,t,i]`，其中 4 routes × 12 runtime mutants；
- 主要增量 `DeltaR[t] = R[B,t] - R[A,t]`；`DeltaR[t] >= 0.20` 的整数等价条件是 B-A 的 route-item 命中净增量至少 10/48；
- 每条 route 的增量为 `(sum_i D[B,r,t,i] - sum_i D[A,r,t,i]) / 12`，至少 3/4 routes 必须严格大于 0；
- `Q[a,t] = (1/48) * sum_r sum_j C[a,r,t,j]`，其中 4 routes × 12 runtime controls；`Q[B,t]-Q[A,t] <= 0.05` 的整数等价条件是候选净增量最多 2/48；
- 每条 route 的新增 control candidates 为 `sum_j I(C[B,r,t,j]=1 and C[A,r,t,j]=0)`，必须不超过 1；
- 两个 runs 必须分别通过全部条件；不得先合并 runs。边界按上述整数比较，不用浮点近似。

FINDING-only、surface 负对照、错误原子主张、tokens、失败重试和人工审计工时均单列，不改变主要 gate。

## Phase 2 冻结前必须补充

Phase 2 可以等待 Phase 1 完成后再合同化，但推理前必须冻结：

- 完整 frame snapshot、stratum 配额、PPS 算法及实现版本、有放回/无放回规则、task 去重、边界单位、随机数、ordered reserve 和每个 revision 的一阶纳入概率；
- 权重重建和抽样重放 verifier，以及与所选设计匹配的方差或重采样方法；
- 对所有 40 个互不重复 task/revision 单元，令 `w_i=1/pi_i`，预注册下界 `L=sum(w_i*I(confirmed))/sum(w_i)`，上界 `U=sum(w_i*I(confirmed or indeterminate or unreachable))/sum(w_i)`；
- determinate-only 比率只可标为条件率，不得因为 determinate 达到 90% 就自动称为总体点估计；任何基于 missing-at-random 等额外假设的估计必须另行预注册。

90% determinate、90% provenance 和“四个 confirmed、跨四个 task”门槛的分母、加权与否、等号边界和 task 去重必须机器化。40 个单位称为“互不重复”，不声称抽样观察在设计上独立。

## Phase 3 冻结前必须补充

Phase 3 的主要估计器改为不依赖小样本回归收敛的直接 item-level risk difference。对 GPT reviewer 的每个 run `t`：

- 对 item `i`，定义 `d[t,i] = D[t,i,GPT-origin] - (1/3) * sum_o D[t,i,o]`，其中 `o` 是三个 non-GPT origins，三者等权；
- `Delta[t] = (1/12) * sum_i d[t,i]`；两个 runs 分开 gate，必须同号且各自 `abs(Delta[t]) >= 0.15`；
- 对每个 run 和每个 item 计算 12 次 leave-one-item-out。若完整估计为正，所有 LOO 必须 `>=0`；若为负，所有 LOO 必须 `<=0`。零不算反向；任何不可估计状态自动 no-go；
- mutation 类别、位置和 generation assignment 由设计平衡并作分层描述，不在主要 gate 中事后切换回归规格；
- control guardrail 只绑定主要 GPT reviewer：每个 run 中，GPT-origin controls 与三个等权 non-GPT-origin controls 的 item-level candidate-rate 绝对差必须 `<=0.10`。其他 reviewers 的 guardrail 只作描述；
- verifier 必须检查 12 个完整 `4 origins × 2 generations` blocks、每个 item 内固定 template、跨 items 的类别/位置平衡、mutant/control assignment、匿名映射和 complete-block estimand 限制。

## 跨阶段继承

Phase 1 的 A/B 结论只产生默认输入政策，不自动证明 B 对所有后续任务适用。Phase 2 和 Phase 3 的 manifest 必须显式记录 `context_policy`：继承 A、继承 B，或因任务结构不适用；后两者都要冻结 source-item 映射、extractor 版本和 missingness 规则，不能在推理后决定。

统一事件层级词典必须区分：claim-level candidate、item-level detection、variant-level control candidate、task-level confirmed residual、真实 control contamination 和 extractor failure。跨阶段同名指标不得绑定不同分子或分母。

## 当前结论

研究顺序保持不变；不存在需要废弃整套方案的致命问题。当前状态是 `READY_FOR_PHASE_1_CONTRACT_AUTHORING`，不是 `READY_FOR_PHASE_1_INFERENCE`。下一步只编写并测试 Phase 1 manifest schema、scorer、extractor contract、gate fixture 和 preflight verifier，不启动模型。
