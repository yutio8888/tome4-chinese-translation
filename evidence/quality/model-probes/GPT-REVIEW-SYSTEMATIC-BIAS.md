# GPT 主导译文审核的系统性偏差风险与研究设计

状态：研究说明；Paseo 分层残余审计 pilot v1 与受控变异 reviewer v1 均已完成。

日期：2026-08-27

## 问题与当前结论

如果译文生成、风险候选筛选、reference 起草、prompt 调整和最终审核基本都由 GPT 或 Codex 完成，那么系统性偏差是现实风险。主要问题不是某一次判断出错，而是多个环节的误差可能高度相关：同一模型族可能反复接受自己惯用的省略、语义压缩和措辞，同时共同忽略不符合其显著性模式的缺陷。因此，多轮 GPT 审核不能直接视为多份独立证据。

当前证据支持“存在至少一个 GPT/Codex 修改并由 GPT/Codex 终审后仍保留的客观机制缺陷”，但尚不能证明这是 GPT 特有的系统性偏差，也不能量化其发生率。历史 B4 上 Codex 的表现最好，既可能来自真实能力优势，也可能部分来自样本、prompt 或 reference 与 GPT 判断方式更一致；现有实验仍不能区分这两种解释。

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

受控变异 reviewer v1 新增了更客观的一层证据：[controlled mutation reviewer v1](controlled-mutation-reviewer-v1/README.md)。Codex 与 GLM 命中 12/12 个预注册变异，Opus 与 Gemini 各命中 11/12；四路 consensus 为 10/12，union 为 12/12。这个结果没有显示 Codex 在注入机制缺陷上出现相对劣势，但只有单次 12 条变异，不能视为模型能力排名或稳定差异。

该实验同时在未变异 C008 中发现了一个固定源码确认的自然缺陷：`FIREBURN` 的 `%d` 是经即时伤害和三回合灼烧分摊的总量，历史终态却写成“每回合造成 %d”。Paseo 快照记录其候选修改者为 GPT/Codex、终态 contextual reviewer 为 GPT/Codex same-family-only；Codex 新路线发现它，Opus 提出正确疑点，GLM 与 Gemini 未提名。它证明同族终审并非独立保护，也证明“历史 DONE 终态”不能直接当 clean control；但它不证明只有 GPT 会漏报，也不足以估算 GPT 系统性偏差率。

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
4. GPT、Claude、GLM、Gemini 等路线使用相同输入、顺序规则、schema 和计分口径独立审核，不交换意见。
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
3. GPT、Claude、GLM、Gemini 独立首审；模型之间不得交换输出。
4. 将 finding 拆成原子主张，隐藏模型身份并随机排序。保留原始输出以便审计，但裁决界面不显示模型来源。
5. 对机制性主张只按固定源码、参数绑定、运行时路径或可复现实验裁决，使用 `confirmed`、`refuted`、`indeterminate` 和 `unreachable`，不强迫不确定项进入二元 reference。
6. 如果存在人工首轮判断，应在展示模型 finding 前锁定；展示后发生的改变另行记录，用于测量意见传播。
7. 结果应称为“模型身份盲化、源码约束的前瞻性裁决”，不得称为独立人工复核。

已有裁决样本可以作为校准题或回归题混入，但必须与新样本分开报告，不能用于估计新语料的残余缺陷率。

## 实验三：Reviewer × Translation Origin 交叉实验

目标是直接检验同族自我偏好，而不是仅比较模型总分。

### 设计

1. 对同一批原文分别生成 GPT、Claude、GLM、Gemini 译文，并保留翻译生成路线。
2. 对不同来源译文注入相同类别、强度和数量的客观可验证变异，同时保留未变异 controls。
3. 隐藏译文来源，让 GPT、Claude、GLM、Gemini 分别审核全部版本。
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

因此，下一步不应继续在 B4 上调整 prompt 来回答系统性偏差问题。受控变异 v1 已证明方法可行，也暴露了 historical-terminal control 的污染风险；应先加强 control 的底层源码核验，并在新机制类别做小型重复。所有主观语言项目在没有外部独立审核者前应保留为 `indeterminate` 或“需要社区复核”，而不是补写成确定 ground truth。

## Paseo 分层残余审计 pilot v1（已完成）

在 provenance snapshot 完成后，已执行一个 20 条探索性 pilot：[Paseo residual audit pilot v1](paseo-residual-audit-pilot-v1/README.md)。抽样先按任务分四层，每层 5 个任务，再从各任务终态 contextual input 确定性抽一条；模型只看到匿名 source、target 和当时冻结的 context。路线为 Codex、Opus、Fable、Opus+Fable Advisor 与 GLM，所有路线均执行完整任务且通过运行时身份和输出门禁。

五条路线的候选联合集只有 H013、H016、H020。固定源码裁决确认 H013 的防御关系错译，驳回 H016 的 source-scope 指控和 H020 的术语指控。唯一确认项的历史链是 GPT 修改、Grok-only contextual review、GPT 编排；历史终态 Grok review 曾把该条标为 `OK`。15 条 GPT-only reviewer 样本未发现确认缺陷，5 条非 GPT-only reviewer 样本发现 1 条。

这个结果不支持“GPT-only reviewer 在本样本留下更多可检测残余缺陷”的窄假设，但不能用于证明 GPT 无系统性偏差：只有模型提名的 3 条经过源码裁决，其余 17 条没有独立逐条核验；每层只有 5 条且题材不匹配；原始译文生成者仍未知；裁决者仍是 GPT/Codex 研究 agent，不是独立人工。Advisor 在本次删除了纯 Opus 的一真一假两条候选，净结果为漏掉唯一确认项。

该 pilot 使下一步优先级更明确：不应继续从小型自然样本推断 reviewer 因果效应。应执行预注册的受控变异 × 译文来源交叉实验，以变异记录和固定源码提供客观标签；自然语料残余率则要等真正的逐条源码审计或外部独立审核资源。

## 受控变异 reviewer v1（已完成）

本实验从未进入上一 pilot 的 P2 终态机制条目中确定性抽取 24 条，对 12 条注入预注册变异，保留 12 条未变异 control；四条活动路线为 Codex GPT-5.6 Sol high、Claude Code Opus 5 medium、Pi/Z.ai CN GLM-5.3 Flash high、agy Gemini 3.7 Flash high。Fable 与 Advisor 因预算退出后续比较，历史 RAW 不删除。

按非 `OK` 且原子主张匹配变异记录的主要口径，Codex 12/12、GLM 12/12、Opus 11/12、Gemini 11/12。Opus 的 C023 为正确 `UNCERTAIN`；若只计 `FINDING`，其结果为 10/12。四路共同命中 10 条，C005 只被 Opus 漏掉，C023 只被 Gemini 漏掉。

未变异 C008 暴露一条真实历史缺陷和一个设计教训。固定源码裁决确认“每回合造成 %d”把 FIREBURN 总伤害误写成逐回合伤害；它由 Codex 提名、Opus 质疑，不计误报。剔除这个被污染 control 后，其余 11 条上四路均无候选。本结果说明：

- 同族 GPT 修改 + GPT 终审确实可能留下一条后续可由固定源码证实的缺陷；
- 新版 Codex 又能发现同一缺陷，因此证据更符合“工作流并非独立且存在具体漏报”，而不是“GPT 必然持续共享同一盲点”；
- 把所有历史 `DONE` 终态当 clean control 会低估自然缺陷并误罚新的 reviewer；
- 单次 12 个注入缺陷不能回答方差、自然缺陷率、语言质量或 reviewer × translation-origin 自我偏好。

预算受限下，下一步应先做小型 fresh-category replication，而不是直接支付四种译文来源 × 四个 reviewer 的完整矩阵。只有在 direct primitive tracing 能把 control 污染降到可接受水平、且重复运行显示差异不是单次波动后，才进入 translation-origin 因子实验。

## UI/日志 fresh-category replication v2（已完成）

小型重复使用 8 条此前未进入 pilot/v1 的 UI 与战斗日志：4 个预注册变异、4 个在推理前完成全目标源码核验的 control。为了避免再次污染 control，Startling Shot 的历史占位符组合先仅在 fixture 中修正，另一个与已选 tooltip 同机制的近重复日志在冻结前排除。四路线和 prompt 判定口径不变。

主要结果为 Codex 4/4、Opus 3/4、GLM 3/4、Gemini 2/4；四路 consensus 2/4，union 4/4。四条 control 在所有路线中均为 `OK`，因此没有 control 污染或误报候选。R007 删除了“机械蜘蛛本身也必须脱离战斗”的条件，只有 Codex 发现；R008 把运行时四回合感知改回过时英文的三回合，Codex/GLM 判 finding，Opus 判 uncertain，Gemini 漏掉。

这次重复改变了研究判断：v1 的近满分不能外推为跨类别稳定能力，模型盲点会随条件主体、运行时优先级和 UI 文本形态变化。Codex 在两个实验中都保持全命中，但总计仍只有 16 个注入变异，且没有同一冻结输入的重复运行，不能据此宣称稳定优势或无系统性偏差。直接源码 control 构造则通过了本轮门禁，说明下一次应优先重复同一 v2 输入来估计随机方差，而不是继续增加新的类别或立即进入 translation-origin 全因子矩阵。

## UI/日志原样 Repeat B（已完成）

已按预注册设计对 v2 的输入、顺序、prompt、schema、模型路线和 effort 做逐字节相同的第二次推理：[controlled mutation UI/log Repeat B](controlled-mutation-ui-log-repeat-b/README.md)。Codex、Opus 与 GLM 原样复现各自 Run A 命中集合，仍分别为 4/4、3/4、3/4；Gemini 则从 2/4 变为 4/4，把此前漏掉的 R007 条件主体和 R008 运行时持续时间都改判为 `FINDING`。16 个路线 × mutation 主指标中有 14 个一致、2 个翻转，一致率 87.5%。四路线的四个直接源码 control 在 A、B 两轮中都全部为 `OK`。

这项结果使“单次模型分数不能作稳定排名”的限制从原则性警告变成了直接观测：Gemini 在完全相同输入上的 mutation recall 从 50% 变为 100%。它不说明 Gemini 已稳定达到满分，也不说明只有 Gemini 有波动；两轮、四个变异不足以估计各路线的方差。Codex 连续两轮 4/4 是正向迹象，但样本仍太小，且仍不回答 reviewer × translation-origin 的同族偏差问题。

预注册规则要求只要出现任一主要检测翻转，就建议一次原样 Run C。因此下一步不应调 prompt 或扩样本，而应先完成第三次相同运行，并以逐条三轮检出频率描述稳定性。Run C 之后再决定是否值得投入 translation-origin 交叉实验；当前证据仍不能证明 GPT 无系统性偏差。
