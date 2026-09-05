# 机械源码上下文受控确认实验报告

实验编号：`source-context-controlled-confirmation-v2`
状态：`COMPLETE / ADOPTION_NO_GO`
执行日期：2026-08-28 至 2026-08-29
适用范围：冻结的 ToME 对话与叙事自然文本有限样本

## 摘要

本实验研究：在项目历史探针语料中未出现、经固定源码核验并在推理前判定为干净的自然文本条目上，加入机械提取的源码上下文，能否稳定提高必须依赖上下文才能判断的受控缺陷检出，同时不损害表面可见缺陷检出，也不增加干净控制项上的客观候选。

实验冻结了 60 个基础条目：24 个上下文依赖 mutant、12 个表面可见 mutant、24 个 clean control；使用 Codex、Opus、GLM、Gemini 四条 CLI 路线，按 `A1 → B1 → B2 → A2` 顺序执行两次重复测量。A 臂仅含 source/target，B 臂唯一增加机械绑定的 `source_context`。60 项被机械分为三个固定 20 项 transport shard；分片不改变样本、顺序、原子、门禁或计分单位。

结果没有支持采用 B 作为默认审核输入。上下文 atom 检出在两次 run 中均描述性净增 10 个 route-item，方向稳定为正，但低于预注册的每轮 `+20/96` 门槛。第一轮完整；第二轮 `A2/GLM/SHARD-01` 因响应包含额外顶层字段而 schema 无效，按协议不可重试，因此第二轮不构成完整配对重复。表面缺陷聚合检出没有下降，但第二轮 Codex 单路线下降 1 个命中。clean control 没有出现 B-only 客观候选，不过复核确认 K014 本身漏译了“主动放任目标成长”的成就条件，构成 control contamination。

因此，本实验提供了“机械源码上下文可能有帮助”的重复正向信号，但没有提供达到预注册效果量、完整性和控制纯度要求的确认性证据。

## 研究问题与决策规则

主要 estimand 是每次 run 内，四条冻结 CLI 路线和 24 个上下文 mutant 上的配对 atom 检出差：

`sum(D[B,r,t,i] - D[A,r,t,i])`

采用 B 必须在两次 run 中分别通过全部门禁：

- 上下文 mutant 净增至少 `20/96`；
- 至少 3/4 路线严格正向，且没有负向路线；
- 表面 mutant 聚合和每路线均不得下降；
- clean control 聚合和每路线候选数不得上升，且不得出现 B-only 新候选；
- base/control contamination 和 mutation-integrity failure 必须为零；
- 所有配对 cell 必须完整、合格；不得插补、不得增加第三轮；
- schema 无效、路线身份不匹配不属于可重试运输失败。

这些规则在正式实验推理前冻结。结果接近边界时也不允许事后放宽门槛。

## 样本构建

### 固定数据边界

- 生产翻译 commit：`1666481409f4c0d63d66e84659f6b6145d8d25d0`
- ToME 固定源码 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
- 初始 source-only screen：240 项，dialogue/narrative 各 120 项
- 最终样本：60 项，30 dialogue、30 narrative
- 最终来源文件：39 个；按预推理修正，单文件最多 3 项
- canonical revision、规范化 source 和 context block 均保持唯一

`project-corpus-novel` 仅表示条目 revision/source 未出现在冻结的已跟踪 model-probe 暴露清单和注册历史终局上下文集合中；它不表示条目不在模型预训练数据、服务端日志或未跟踪历史会话中。

### clean audit

候选先进行 surface-only 审核，再释放机械源码上下文进行 context 审核。主样本与 narrative reserves 共审核 180 项；只有两次审核均为 CLEAN、且 lead adjudication 为 `CLEAN_NO_MATERIAL_DEFECT` 的条目进入最终候选池。

推理后发现 K014 实际并不干净，说明该多阶段 clean audit 仍存在假阴性。这个发现被记为 control contamination，而没有事后替换控制项。

### 受控 mutation

- 上下文依赖 mutant：24 项，dialogue/narrative 各 12 项
- 表面可见 mutant：12 项，dialogue/narrative 各 6 项
- clean control：24 项，dialogue/narrative 各 12 项

上下文 mutation 在 A-only manipulation check 中必须无法由 source/target 客观判错，在 B-context check 中必须能被固定上下文唯一反驳。最终上下文家族分布为：

- speaker/addressee 或 agent/patient：3
- referent/entity identity：8
- event/branch/condition/scope：10
- direction/polarity/ownership：3

原计划每个家族 6 项，但预推理 manipulation-eligible proposals 无法诚实满足这一配额；`DESIGN-AMENDMENT-006.json` 保留了修正及理由。主要结论仍针对 24 项聚合，家族结果仅可描述。

## 请求、路线与执行

### 盲化与 A/B 控制

模型请求不包含原始 `C/S/K` 角色 ID、role、mutation family、proposal、audit、revision、路径、哈希或 sealed reference。60 项使用冻结中性 ID `Q001–Q060` 和固定打乱顺序。

每个 shard 中：

- A1 与 A2 请求逐字节相同；
- B1 与 B2 请求逐字节相同；
- A/B 的唯一条目字段差异是 B 多出 `source_context`；
- canonical JSON schema 原始字节嵌入所有路线共同请求；原生 schema 参数仅作为额外约束。

### 分片修正

首次非研究资格夹具使用单个 60 项请求。Gemini 运输成功并消耗输出 token，但未产生 structured envelope；正式 B 请求当时约 829 KB。为避免把长请求和序列化失败混入“上下文是否有帮助”的处理效应，正式推理前登记 `DESIGN-AMENDMENT-007.json`，将冻结顺序机械切成三个连续 20 项 shard。

20 项资格重跑中四条路线全部通过。原 60 项资格失败记录被保留，没有计入模型成绩。

### 冻结路线

| 路线 | CLI 版本 | 请求模型与 effort | 身份证据层级 |
|---|---|---|---|
| Codex | 0.150.1 | `gpt-5.6-sol`, high | requested-route-only；envelope 不独立证明运行时模型 |
| Opus | 2.1.251 | `claude-opus-5`, medium | init、assistant、modelUsage 均要求只含 Opus，无 advisor/fallback |
| GLM | 0.84.3 | `zai-standard-cn/glm-5.3-flash`, high | terminal provider/model 必须精确匹配 |
| Gemini | 1.1.22 | `gemini-3.7-flash-high`, high | requested-route-only；envelope 可不报告 model |

比较对象是完整 CLI route intervention，而不是纯粹的底层模型能力。尤其不能把 Codex/Gemini 的 requested route 当成已由运行时遥测独立证明的模型身份。

### 实际执行

- 正式运输调用：48 个（4 waves × 4 routes × 3 shards）
- 严格解析有效：47 个
- 无效：1 个，`A2 / GLM / SHARD-01`
- 正式实验重试：0
- 第三轮：0

唯一无效响应包含 schema 未允许的额外顶层字段。它已有非合成 assistant payload，因此不符合“无 assistant payload 才允许一次字节相同重试”的条件。

## 主要结果

| Run | 上下文 A→B | 净增 | 正向/负向路线 | 表面 A→B | clean A→B | 完整 |
|---|---:|---:|---:|---:|---:|---|
| 1 | `6→16 / 96` | `+10` | `3 / 0` | `23→27 / 48` | `1→1 / 96` | 是 |
| 2 | `4→14 / 96` | `+10` | `4 / 0` | `26→28 / 48` | `1→1 / 96` | 否 |

第二轮聚合包含无效 GLM A shard 导致的不完整机会集，只能作为 scorer 保留的描述性总数，不能视为完整配对估计。即使只看完整的第一轮，`+10` 也未达到 `+20` 门槛；control contamination 也独立使采用失败。

### 门禁结果

第一轮失败：

- 上下文净增未达到 20；
- control contamination 不为零。

第二轮失败：

- 配对 cell 不完整；
- 上下文描述性净增未达到 20；
- Codex 表面 mutant 检出下降 1；
- control contamination 不为零。

通过的保护信号包括：两轮均没有负向 context 路线、context 正向路线数达到要求、表面聚合未下降、clean 候选没有净增、没有 B-only clean 候选、没有已知 mutation-integrity failure。

## 四条审核路线的表现

| 路线 | Run 1 context A→B | Run 2 context A→B | Surface 变化 | 最终客观 clean 候选 | 观察 |
|---|---:|---:|---:|---:|---|
| Codex | `0→3` | `0→1` | `+3`, `-1` | 两轮均命中 K014 | 较激进，能发现污染项，但波动和非实质提名较多 |
| Opus | `4→4` | `3→5` | `0`, `0` | 0 | A-only 基线较强，表面检出最稳定，上下文增益较小 |
| GLM | `1→2` | 不可正式比较 | `0`, 不可正式比较 | 0 | 较保守；第二轮 A shard 无效，稳定性证据不足 |
| Gemini | `1→7` | `1→6` | `+1`, `+2` | 0 | 本样本中上下文增益最大，且未提名 clean control |

Gemini 的两轮上下文净增分别为 `+6`、`+5`，是本实验中最明确的上下文受益路线。Opus 的 A-only 命中较高，加入上下文后的边际提升较小，但输出稳定。Codex 提名 clean 项最多，同时也是唯一反复发现 K014 真污染的路线，表现出高敏感度与较高审查成本。GLM 第一轮只有小幅正增，第二轮因 schema 无效不能作正式配对评价。

这些比较只描述当前冻结样本、prompt、schema、CLI 版本和 effort；不能直接推断一般性的模型排名。

## clean control 复核

有效响应共产生 23 条 clean-control nomination：Codex 12、Opus 8、GLM 3、Gemini 0。按固定 source/target 复核后：

- K014 的 4 次提名被判定为 `CONTROL_CONTAMINATION`；
- 其余 19 条被判定为 `STYLE_OR_UNSUPPORTED`，主要涉及非实质状语省略、可接受释义或专名偏好；
- 没有 B-only 客观 clean candidate。

K014 的英文要求在“让她成长到尽可能强大之后”击杀，中文只表达“她成长之后”，遗漏玩家主动放任这一条件。它不应被继续用作干净控制；但当前实验不替换该项，也不重新计算一个假想的清洁版本。

## 解释

实验支持三个较弱结论：

1. 机械源码上下文在两次执行中都提高了聚合 atom 检出，且没有任何路线出现 context 负向差值。
2. 收益高度依赖路线：Gemini 的收益明显，Opus 和 GLM 较小，Codex 介于两者之间且有波动。
3. 上下文没有在本样本中制造新的 B-only clean 客观候选，但 clean-audit 本身未能保证控制纯度。

实验不支持以下更强结论：

- 不支持把源码上下文设为四路线统一默认输入；
- 不支持“稳定达到实用效果量”的确认性结论；
- 不支持对第二轮作完整配对推断；
- 不支持将结果外推到 mechanics、UI、runtime log、DLC 或全仓库自然缺陷；
- 不支持将路线差异解释为纯底层模型差异。

## 局限与异常记录

1. 最终上下文 mutation family 不均衡，condition/scope 和 referent 类占多数。
2. 单个冻结 control 的污染足以破坏零污染门禁，也说明双阶段 clean audit 仍需要更强的确定性或独立复核。
3. GLM 的结构化输出可靠性导致第二轮一个 paired cell 缺失。
4. Codex 与 Gemini 的 CLI envelope 没有提供与 Opus/GLM 同等级的运行时模型身份证据。
5. scorer 使用严格的 target-span、claim-type 和 correction-anchor matcher；它优先保证可复核性，可能漏掉语义正确但修正措辞不满足锚点的候选。
6. 分片是运输实现，不是独立样本；不能把 shard、route-item 或重复 run 当作独立随机抽样单位。
7. 冻结 scorer 原本预期最终 clean adjudication 覆盖队列文件。为同时保留队列和最终裁决，RAW 冻结后、计分前只修正了读取路径，并以 `SCORER-IO-ERRATA-001.json` 绑定旧、新 scorer 哈希；计分逻辑和门禁未改变。

## 后续实验建议

1. 新建版本而不是修改本实验。对新候选增加第三个独立 clean pass，特别检查条件主体、因果和成就触发语义；K014 必须排除于新 clean frame。
2. 在新的、未参与本次 prompt 和 matcher设计的样本上复现，并保持预注册门槛不变，以判断 `+10` 是否稳定还是本有限集特征。
3. 将 Gemini-style context reviewer 与 Opus-style稳定 reviewer 作为预注册角色变量，比较单路线默认、两路线 union 和主席复核；不要根据本次结果直接挑选命中项调参。
4. 单独开展结构化输出可靠性实验，解决 GLM schema drift；可靠性资格必须使用非研究 fixture，不得通过重采样正式 cell 修复。
5. 报告 matcher sensitivity analysis 时使用冻结 RAW 离线重算，并把它标成次级分析；不得覆盖当前主结果。
6. 若未来想降低 `+20` 门槛，必须基于成本收益或独立 pilot 另行预注册，不能用本次 `+10` 结果倒推新阈值。

## 可复核产物

- 设计与修正：[`DESIGN-CONTRACT.json`](DESIGN-CONTRACT.json)、[`DESIGN-AMENDMENT-007.json`](DESIGN-AMENDMENT-007.json)
- 最终样本与 sealed truth：[`FINAL-SAMPLE.json`](FINAL-SAMPLE.json)、[`SEALED-REFERENCE.json`](SEALED-REFERENCE.json)
- 路线资格：[`ROUTE-REGISTRY.json`](ROUTE-REGISTRY.json)
- 请求冻结：[`FROZEN-HASHES.json`](FROZEN-HASHES.json)、[`SHARDED-REQUEST-BUILD-REPORT.json`](SHARDED-REQUEST-BUILD-REPORT.json)
- matcher 与控制裁决：[`ATOM-MATCHERS.json`](ATOM-MATCHERS.json)、[`CLEAN-CANDIDATE-ADJUDICATION-FINAL.json`](CLEAN-CANDIDATE-ADJUDICATION-FINAL.json)
- 完整计分与结论：[`SCORES.json`](SCORES.json)、[`RESULT.json`](RESULT.json)
- 最终核验：[`FINAL-VERIFICATION.json`](FINAL-VERIFICATION.json)
- scorer 路径修正：[`SCORER-IO-ERRATA-001.json`](SCORER-IO-ERRATA-001.json)

`RESULT.json` SHA-256：`0dd239c7d7eeecb82d871bfc8bc99b97ee3967d096059462526d5cdaf4e2669c`
`SCORES.json` SHA-256：`798fa423876c2f9515d278a8fdadfd9036eb62ed8bbd145f736e777fee4dca14`

本报告记录已完成实验，不构成正式翻译修改裁决，也不将模型候选提升为生产仓库 finding。
