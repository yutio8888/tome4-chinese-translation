# GPT 主导译文审核的系统性偏差风险与研究设计

状态：研究说明；Paseo 分层残余审计 pilot v1 已完成，受控变异实验尚未执行。

日期：2026-08-27

## 问题与当前结论

如果译文生成、风险候选筛选、reference 起草、prompt 调整和最终审核基本都由 GPT 或 Codex 完成，那么系统性偏差是现实风险。主要问题不是某一次判断出错，而是多个环节的误差可能高度相关：同一模型族可能反复接受自己惯用的省略、语义压缩和措辞，同时共同忽略不符合其显著性模式的缺陷。因此，多轮 GPT 审核不能直接视为多份独立证据。

当前证据只支持“需要专门排查该风险”，尚不能证明偏差已经发生，也不能量化其大小。历史 B4 上 Codex 的表现最好，既可能来自真实能力优势，也可能部分来自样本、prompt 或 reference 与 GPT 判断方式更一致；现有实验不能区分这两种解释。

## 当前证据链的保护与局限

现有研究已经提供两项重要保护：

- B4 reference 为每项裁决记录固定源码位置和机制证据，而不是只依赖语言直觉：[p1-b4-s2-verification.json](../p1-batches/p1-b4-s2-verification.json)。
- 模型推理时不读取 sealed reference，reference 只在输出完成后由本地计分器读取。

但这些保护不能证明 ground truth 独立于 GPT。现有记录没有为每项译文完整标注译文生成者、候选发现者、reference 起草者、源码核验者和最终裁决者，因而无法完整重建各阶段的模型家族相关性。

Paseo 本机记录现已整理为一份可跟踪重建的脱敏快照：[Paseo provenance snapshot v1](paseo-provenance-snapshot-v1/README.md)。它能重建 contextual-review 任务中的编排者、候选修改者、正式 reviewer、dispatch 轮次、review artifact 和部分交付 commit，但不能识别 read-and-fix 之前的原始译文生成者。

快照清点了 128 个完成任务：P1 的 8 个完成任务没有 GPT reviewer；P2 的 120 个完成任务中，113 个包含 GPT reviewer，107 个只出现 GPT reviewer。全部完成任务中，候选修改者归因有 113 个为 GPT/Codex；96 个任务是已解析候选修改者与 reviewer 同族 only。这个结果把风险定位为“P2 中候选修改和正式审核高度同族相关”，而不是“全部历史审核都由 GPT 完成”。它仍然不能证明偏差已经发生，因为任务编排者有 Claude/Grok，Paseo 候选修改者也不是原始译文生成者，且 reference/source adjudication 的作者链仍不完整。

当前模型比较也显示不同路线存在互补盲点：

- 历史 B4 Codex baseline 的召回率为 57.14%，仍漏掉 3/7 个固定缺陷：[non-args reviewer comparison](non-args-reviewer-model-comparison-b4-v1/RESULT.json)。
- Opus、Fable 与 GLM 的命中集合不同；没有任何新路线覆盖全部缺陷：[new route comparison](claude-opus-fable-5-reviewer-b4-v1/COMPARISON.json)。
- Opus 加 Fable Advisor 后混淆矩阵不变，却丢失一个原有 true positive 并获得另一个 true positive。相同总分会掩盖不同的盲点。

这些现象说明单模型审核不足，但不构成 GPT 系统性偏差的直接证据。

## 可能的偏差路径

| 偏差路径 | 可能后果 |
| --- | --- |
| 同族自洽偏差 | GPT 更容易接受 GPT 风格译文中的省略、语义压缩或惯用改写，形成相关漏报。 |
| 候选选择偏差 | 样本主要来自 GPT 认为可疑的内容，GPT 没有注意到的缺陷不会进入 reference 或评测集。 |
| Reference 内生性 | 如果 defect 定义和 reference 主要由 GPT 起草，GPT 在该基准上可能天然更匹配。 |
| 风格偏好偏差 | 非 GPT 风格但正确的中文可能被误报；流畅但语义偏移的 GPT 风格译文可能被接受。 |
| Prompt 过拟合 | 根据 GPT 或特定模型在开发集上的表现调整 prompt，可能把该模型的推理习惯编码进评测。 |
| 相关盲点 | 多次同族复审可能重复遗漏运行时机制、条件主体、范围边界、社区术语或文化语气问题。 |
| 计分契约偏差 | 严格字符串标签或解析规则可能把模型的真实语义判断映射成另一类别；这不是 GPT 特有偏差，但会混淆比较。 |

## 独立人工审核者缺失这一限制

目前没有不知道历史结论的独立人工审核者。让已参与项目的人看不到 revision ID、打乱样本顺序或暂时隐藏旧记录，只能降低锚定效应，不能使其成为真正独立的审核者。因此，不应把这种安排描述为“独立人工复核”。

需要区分两种情况：

1. 对已有裁决条目，参与者可能记得结论或已经受旧结论影响。它们只能用于回归、协议开发和敏感性分析，不能用来证明不存在 GPT 偏差。
2. 对尚未进行条目级审核的新随机样本，参与者虽然熟悉项目，但不知道条目级历史答案。可以实施前瞻性、模型身份盲化、源码约束的单人裁决，但仍必须如实记录它不是独立人工 ground truth。

匿名化可以控制模型声望和顺序影响，不能消除裁决者自身的历史经验。多模型多数票也不能替代 ground truth，因为模型错误并不独立。

## 实验一：受控变异审核

目标是检测审核器对客观机制错误的系统性盲点，不依赖新的人工语言 reference。

### 设计

1. 从能够通过固定源码或确定性检查确认的正确译文建立 clean controls。不能仅凭旧 GPT 的 `correct` 标签选取基线。
2. 预先冻结变异规则和随机种子，再生成 defect variants。候选变异包括：
   - 调换格式化参数或数值对应关系；
   - 删除伤害、持续时间或资源消耗的参照量；
   - 反转、扩大或缩小条件范围；
   - 改变条件所修饰的主体；
   - 删除一个并列效果或将两个不同机制合并；
   - 添加源码中不存在的机制、状态或限制。
3. 每个 clean control 与对应 defect variant 成对保存，但向模型隐藏配对关系、变异类型和标签。
4. GPT、Claude、GLM 等路线使用相同输入、顺序规则、schema 和计分口径独立审核，不交换意见。
5. ground truth 来自冻结的变异记录和固定源码；先计分，再揭示变异类型。

### 可以回答的问题

- 各审核器对不同客观缺陷类别的漏报率和误报率；
- GPT 是否特别容易漏掉某种由 GPT 风格表述承载的机制错误；
- 不同模型的盲点是否互补，以及 union 增加的候选中有多少由确定性证据支持。

### 不能回答的问题

人工注入缺陷的分布可能不等同于真实译文缺陷，因此该实验不能直接估计现有语料的自然残余缺陷率，也不能裁决文采、语气或母语自然度。

## 实验二：未审样本的前瞻性源码审计

目标是估计 GPT 主导流程在此前未作条目级裁决的语料中留下多少可由源码确认的缺陷。

### 设计

1. 在查看模型输出前冻结抽样总体、排除规则、随机种子、样本清单、prompt、schema 和计分方案。
2. 从未进入历史 finding、verification 或 prompt 开发集的语料中确定性随机抽样。不能只抽取 GPT 风险筛选器命中的条目。
3. GPT、Claude、GLM 独立首审；模型之间不得交换输出。
4. 将 finding 拆成原子主张，隐藏模型身份并随机排序。保留原始输出以便审计，但裁决界面不显示模型来源。
5. 对机制性主张只按固定源码、参数绑定、运行时路径或可复现实验裁决，使用 `confirmed`、`refuted`、`indeterminate` 和 `unreachable`，不强迫不确定项进入二元 reference。
6. 如果存在人工首轮判断，应在展示模型 finding 前锁定；展示后发生的改变另行记录，用于测量意见传播。
7. 结果应称为“模型身份盲化、源码约束的前瞻性裁决”，不得称为独立人工复核。

已有裁决样本可以作为校准题或回归题混入，但必须与新样本分开报告，不能用于估计新语料的残余缺陷率。

## 实验三：Reviewer × Translation Origin 交叉实验

目标是直接检验同族自我偏好，而不是仅比较模型总分。

### 设计

1. 对同一批原文分别生成 GPT、Claude、GLM 译文，并保留翻译生成路线。
2. 对不同来源译文注入相同类别、强度和数量的客观可验证变异，同时保留未变异 controls。
3. 隐藏译文来源，让 GPT、Claude、GLM 分别审核全部版本。
4. 以源码和受控变异记录作为 ground truth，比较审核器与译文来源之间的交互效应。

主要问题是：控制缺陷类别和条目难度后，GPT 审核 GPT 来源译文的漏报率是否显著高于它审核其他来源译文的漏报率。若出现稳定的 reviewer × origin 交互，才是比“Codex 总分较高”更强的同族偏差证据。

该实验仍只能裁决客观变异。没有真正独立的母语审核者时，不能据此宣称某个模型在文采、社区习惯或文化语气方面更好。

## 计量与报告要求

主要报告：

- 按缺陷类别和译文来源分层的 recall、precision、clean false-positive rate 和 balanced accuracy；
- reviewer × translation-origin 的交互效应；
- 每个模型的独有 finding、经源码确认的独有 finding，以及 union/consensus；
- 新随机样本中的残余 confirmed defect rate；
- `indeterminate` 与 `unreachable` 比例；
- 人工判断在看到匿名模型 finding 前后的变化；
- 重复完整运行的方差，而不是简单任务 smoke 的路由结果。

Union、consensus 和多模型讨论只能作为派生候选生成策略，不得按多数机械裁决。若讨论实验允许模型互相查看意见，应与独立首审结果分开报告意见传播。

## 需要补充的 provenance

后续样本和 reference 至少记录：

- `translation_generator` 与模型/版本；
- `candidate_selector`；
- `first_reviewer`；
- `reference_drafter`；
- `source_verifier`；
- `final_adjudicator`；
- 每一阶段是否知道模型身份或历史结论；
- prompt、输入、源码 commit 和工具版本哈希；
- finding 属于客观机制、术语一致性、语言自然度还是主观风格。

这些字段用于判断证据链是否真正跨模型独立，也用于防止把 GPT 发现、GPT reference 和 GPT 复审误当成三份独立证据。

## 当前可作与不可作的结论

在没有独立人工审核者的条件下，可以较可靠地研究：

- 客观机制错误的检测能力与系统性盲点；
- 同一受控缺陷在不同译文来源上的漏报差异；
- 未审随机样本中可由源码确认的残余缺陷；
- 多模型候选生成的互补性和成本。

目前不能独立裁决：

- 整体中文文采和母语自然度；
- 社区术语偏好和角色语气；
- 需要文化解释而没有固定证据的争议；
- “GPT 审核总体无偏”或“某非 GPT 模型总体更公正”。

因此，下一步不应继续在 B4 上调整 prompt 来回答系统性偏差问题。应先建立新的、未参与设计的前瞻性 holdout，并并行建立受控变异集。所有主观语言项目在没有外部独立审核者前应保留为 `indeterminate` 或“需要社区复核”，而不是补写成确定 ground truth。

## Paseo 分层残余审计 pilot v1（已完成）

在 provenance snapshot 完成后，已执行一个 20 条探索性 pilot：[Paseo residual audit pilot v1](paseo-residual-audit-pilot-v1/README.md)。抽样先按任务分四层，每层 5 个任务，再从各任务终态 contextual input 确定性抽一条；模型只看到匿名 source、target 和当时冻结的 context。路线为 Codex、Opus、Fable、Opus+Fable Advisor 与 GLM，所有路线均执行完整任务且通过运行时身份和输出门禁。

五条路线的候选联合集只有 H013、H016、H020。固定源码裁决确认 H013 的防御关系错译，驳回 H016 的 source-scope 指控和 H020 的术语指控。唯一确认项的历史链是 GPT 修改、Grok-only contextual review、GPT 编排；历史终态 Grok review 曾把该条标为 `OK`。15 条 GPT-only reviewer 样本未发现确认缺陷，5 条非 GPT-only reviewer 样本发现 1 条。

这个结果不支持“GPT-only reviewer 在本样本留下更多可检测残余缺陷”的窄假设，但不能用于证明 GPT 无系统性偏差：只有模型提名的 3 条经过源码裁决，其余 17 条没有独立逐条核验；每层只有 5 条且题材不匹配；原始译文生成者仍未知；裁决者仍是 GPT/Codex 研究 agent，不是独立人工。Advisor 在本次删除了纯 Opus 的一真一假两条候选，净结果为漏掉唯一确认项。

该 pilot 使下一步优先级更明确：不应继续从小型自然样本推断 reviewer 因果效应。应执行预注册的受控变异 × 译文来源交叉实验，以变异记录和固定源码提供客观标签；自然语料残余率则要等真正的逐条源码审计或外部独立审核资源。
