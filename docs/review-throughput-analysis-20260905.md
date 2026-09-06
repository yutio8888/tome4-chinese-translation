# 正式审核流程吞吐分析（2026-09-05）

本文是一份只读分析报告，对截至 `8f2f0c9` 的 `production-review-v2-lite` 正式审核流程做
定量诊断，并给出按收益排序的改进项。**本文不修改任何契约、策略或审核结论**；文中所有
派生数字均可由附录脚本从受跟踪证据重算，不属于 adjudicated evidence，不得写入
`evidence/`，也不能当作任何条目的审核结论。

分析对象是 38 个已提交批次（`evidence/production-review-v2-lite/batches/`）共 2,327 条
结果，其中 2026-09-05 恢复后连续运行的 20 批共 887 条为主要观测窗口。

---

## 0. 摘要

| 结论 | 证据 |
| --- | --- |
| 周期时间与批量几乎无关 | `r(批量, 周期) = 0.10`；2 条批 21 分钟，80 条批 22 分钟 |
| 门禁不是瓶颈 | 17 项门禁平均 82 秒，占周期 6.2% |
| 按源码身份切批浪费了约 35% 的批次 | 9/20 批 <30 条，占 12% 产出、45% 批次；同序重排为 13 批 |
| 周期时间在单会话内漂移 +50% | 19→29 分钟，`r(批次序号, 周期) = 0.92` |
| 优先键已退化为近似随机序 | rank-1 的 68 条已全部审完；剩余 89.7% 的次级键取同值 |
| 表层产出率出现断层 | 恢复前 126 ISSUE / 1,440 条（8.75%），恢复后 0 / 887 |
| 一类可确定性判定的缺陷仍在走 LLM 审核 | 全量正则扫描 <1 秒命中未审的 1,521 条（5.5%），lint 不覆盖 |
| 已 OK 条目中存在同类未判定模式 | 887 条中 11 条带早期已 confirmed 的同型模式 |
| 剩余工作中约 16% 为完全重复文本 | 3,465 条组内重复 + 1,006 条已在别处审过 |

按当前实测速率（122 条/小时），剩余 27,602 条约需 **227 小时**。仅落实无需授权的第
1、3 项，可降到约 127 小时；若同时提升批量上限，可进一步降低，但幅度取决于一项本文
最初遗漏的约束（见 §11 的修正说明与[批量上限升级提案](production-review-batch-limit-upgrade-proposal-v1.md)）。

---

## 1. 数据来源与方法

| 数据 | 来源 |
| --- | --- |
| 批次规模、ISSUE、裁决数 | `evidence/production-review-v2-lite/batches/*/results.jsonl`、`adjudications.jsonl` |
| 门禁逐项耗时 | 各批 `gates.json` 的 `result.checks[].started_at/finished_at`（schema 2） |
| 批次周期 | 相邻批次 `gates.json` 的 `result.started_at` 之差 |
| 语料与风险字段 | `evidence/production-review-v2-lite/catalog/entries.jsonl`（29,828 条） |
| 排序规则 | `tools/i18nlib/production_review_v2_lite_batch.py:197` 的 `_risk()` |

**方法上的三点声明。** 第一，"周期"以门禁开始时刻之差度量，是批次总时长的代理量，包含
选片、冻结、派发、导入、裁决、提交、交接的全部时间，但首批之前的准备时间不在窗口内。
第二，附录的机械扫描产出的是**候选**，不是缺陷；按 AGENTS.md 的校对判定依据，任何一条
都必须经固定源码裁决后才能成为 finding。第三，本文的相关系数样本量为 19，只用于区分
"强相关/无相关"这一量级判断，不作更细推断。

---

## 2. 观察一：周期时间与批量无关

恢复后 20 批的实测（`n` 为条目数，`gate_s` 为该批 17 项门禁总秒数）：

| # | batch | n | gate_s | 门禁开始 | 周期(分) |
| ---: | --- | ---: | ---: | --- | ---: |
| 1 | `batch-41de8748` | 80 | 77 | 07:47:05 | — |
| 2 | `batch-5ebe7845` | 78 | 79 | 08:07:41 | 21 |
| 3 | `batch-5a2b6401` | 12 | 105 | 08:27:17 | 20 |
| 4 | `batch-40c65c69` | 48 | 82 | 08:46:56 | 20 |
| 5 | `batch-d0aae8bc` | 80 | 80 | 09:06:05 | 19 |
| 6 | `batch-d960f8e6` | 8 | 86 | 09:24:19 | 18 |
| 7 | `batch-7aa51896` | 2 | 77 | 09:44:52 | 21 |
| 8 | `batch-ba4a4d4e` | 9 | 79 | 10:04:38 | 20 |
| 9 | `batch-7e79a3c5` | 18 | 79 | 10:25:17 | 21 |
| 10 | `batch-7fc4cb3b` | 80 | 79 | 10:47:40 | 22 |
| 11 | `batch-96f2172d` | 80 | 83 | 11:09:33 | 22 |
| 12 | `batch-56f5ca2f` | 80 | 83 | 11:32:09 | 23 |
| 13 | `batch-2f69451d` | 24 | 83 | 11:54:04 | 22 |
| 14 | `batch-046aa45b` | 6 | 84 | 12:19:34 | 26 |
| 15 | `batch-a287c35e` | 27 | 82 | 12:44:34 | 25 |
| 16 | `batch-f164b5b9` | 54 | 82 | 13:10:53 | 26 |
| 17 | `batch-1e8f1c82` | 80 | 83 | 13:38:13 | 27 |
| 18 | `batch-40e8c319` | 80 | 79 | 14:06:52 | 29 |
| 19 | `batch-6af04961` | 38 | 79 | 14:36:05 | 29 |
| 20 | `batch-e07e805f` | 3 | 84 | 15:05:07 | 29 |

- `r(批量, 周期) = 0.10`——无相关。
- 批量 ≥48 的 9 批平均 **23.2 分钟**；批量 <30 的 9 批平均 **22.4 分钟**。小批并没有更快。

**成本结构结论：** 单条边际成本接近 0，成本几乎全部是每批固定开销（选片与逐条固定源码
核验、SPEC/PLAN/SCOPE/STATE、四路派发与等待、结果导入与校验、门禁、提交、交接文档）。
因此**批次数量是唯一有意义的成本变量**，任何优化都应当以"减少批次数"而非"减少每批工作"
为目标。这一点也解释了为什么至今所有优化努力的边际收益都不明显。

---

## 3. 观察二：门禁不是瓶颈

20 批的 17 项门禁逐项平均耗时：

| 检查 | 平均 |
| --- | ---: |
| `05-production-shadow-surface-ledger-tests` | 33.1s |
| `03-toolchain-unit-tests` | 26.2s |
| `04-quality-facts-unit-tests` | 10.7s |
| `05-contract-suite-unit-tests` | 7.6s |
| `12-core-addon-build`（严格 build） | 1.1s |
| `09-terminology-dynamic-audit` | 1.1s |
| `02-strict-lint` | 0.8s |
| 其余 10 项合计 | < 1.5s |

单批总计平均 82 秒（最慢 105 秒），20 批合计 27 分钟，占 7.3 小时窗口的 **6.2%**。

**结论：** 不要把优化力气花在门禁上。严格 addon build 只要 1.1 秒，`--skip-build` 这类
豁免在吞吐上毫无意义，反而削弱保证——应当继续保持每批全量门禁。四项单元测试合计 78 秒
占了门禁的 95%，即使全部砍掉也只省下不到 1.5% 的总时间，不值得动。

---

## 4. 观察三：按固定源码身份切批浪费了约 35% 的批次

20 批里有 9 批小于 30 条（2、3、6、8、9、12、18、24、27 条），合计 109 条——**12% 的产出
占用了 45% 的批次**，按平均 22.4 分钟计约 3.4 小时。

这些小批全部来自同一个原因：交接文档反复记录的"下一连续源码身份切片"，即在
`fixed_source_identity` 变化处截断批次。

**这不是契约要求。** `docs/translation-production-review-v2-lite-plan.md:266` 明确规定：

> 一个 active batch 可以混有不同 `fixed_source_identity`；adapter 按
> `(fixed_source_identity, terminology_snapshot_sha256, rules_version)` 精确值分组。
> 每个同质 run 的 membership 是 parent selected 中对应 entries 的有序子序列……
> validator 必须证明各 run 不相交，每条 parent identity 恰出现一次。

也就是说，同质性要求作用在 **run** 层，不作用在 **batch** 层，且拆分由 adapter 自动完成
并由 validator 证明守恒。混合身份批次是被设计支持的路径，按身份切批是一项自我施加的
额外约束，它把 run 级的同质性要求错误地上提到了 batch 级。

**影响估算：** 保持完全相同的队列顺序、完全相同的 887 条内容，只按 80 条上限贪心装箱，
需要 **13 批**（理论下限 12 批）而不是实际的 20 批。按 22.4 分钟/批计，同样产出可省下
约 **2.6 小时（-35%）**。

代价：每批需要运行多次 `surface_screen_manifest.py`（每个同质 run 一次），派发的 child
数量在 run 数 >1 时上升。但 child 派发是并行的，而批次是串行的——这正是应当做的交换。

---

## 5. 观察四：周期时间在单会话内漂移 +50%

周期从第 2 批的 21 分钟单调上升到第 20 批的 29 分钟，`r(批次序号, 周期) = 0.92`。前 9 个
周期均值 20.2 分钟，后 10 个 25.8 分钟。同期门禁耗时**没有**上升（77–86 秒，无趋势），
批量也没有系统性变化，因此漂移来自门禁以外的编排环节。

最可能的成因是交接文档的只增结构：`docs/production-review-handoff-2026-09-05.md` 现有
20 个结构雷同的"第 N 批完成"小节，每批都要通读并追加一节。而这些小节记录的内容
（批次 ID、提交哈希、S/D/R/I 计数、门禁通过）在 `batches/*/manifest.json` 与队列投影里
已经是可重算的持久证据，文档中的副本是第二份真相来源。

**建议：** 把交接文档压缩为"当前基线 + 当前队列状态 + 恢复步骤 + 停下条件"，逐批叙事
改为指向 `batches/` 的指针。历史小节可整体移入一份归档文档而不是删除。这项改动不触及
任何契约，属于纯文档整理。

需要说明的是，本项归因尚未被实验证实——确认方式很简单：压缩文档后观察后续 5 批的周期
是否回落到 20 分钟一线。

---

## 6. 观察五：优先键已经退化为近似随机序

`tools/i18nlib/production_review_v2_lite_batch.py:197` 的排序键：

```python
(-int(bool(risk["has_args_order"] or risk["has_special"])),
 -risk["component_group_size"],
 -int(bool(risk["component_group_last"])),
 ordinal.get(row["component"], 999),          # engine=0, boot=1, tome=2, ……
 row["entry_revision_identity"])
```

对剩余的 27,602 条实测：

- 第一键：全语料仅 **68** 条满足 `has_args_order or has_special`（`has_special` 为 0 条），
  且这 68 条**已全部审完**，剩余条目该键恒为同值。
- 第二键：剩余条目中 `component_group_size=1` 的有 **24,766 条（89.7%）**，`=2` 的 2,260 条，
  `=3` 的 576 条——近乎恒定。
- 第三键同样近乎恒定。

因此实际生效的排序退化为"组件序 + `entry_revision_identity` 哈希序"，即**对缺陷概率而言
是随机序**。这意味着：审核推进顺序当前不携带任何风险信息，先审的和后审的条目期望缺陷率
相同，无法通过"先做高价值部分"获得任何早期收益。

这一点同时给观察六提供了一个更简单的解释。

---

## 7. 观察六：表层产出率断层

按 `recorded_at` 排序的 ISSUE 产出：

| 阶段 | 批次 | 条目 | ISSUE | 裁决 |
| --- | ---: | ---: | ---: | ---: |
| 恢复前（09-02 ~ 09-04） | 18 | 1,440 | 126（8.75%） | 198 |
| 恢复后（09-05） | 20 | 887 | **0** | 0 |

恢复前本身也是高度集中的：`batch-c7f8a5c7` 一批 66 条 ISSUE、`batch-d1ac61da` 24 条，两批
占 126 条中的 90 条；其余批次多为 0–8 条。最后一个非零批是 09-04T22:38 的 4 条 ISSUE，
之后连续 20 批为 0。

**两种假设。**

- **H1（良性）：** 队列已走出早期人工翻译密集区，进入结构化、重复度高的批量文本；观察五
  说明推进顺序对缺陷概率无信息，早期的集中命中来自内容分布而非排序，因此零产出区段是
  可能的。观察九（16% 为完全重复文本）支持这一点。
- **H2（风险）：** 表层筛查的灵敏度下降，reviewer 在长期全 OK 的语境下趋于盖章。

现有证据不能区分二者，而观察八提供了一点偏向 H2 的迹象。这个问题必须在提升批量上限
**之前**回答：若 H2 成立，扩容会把无效审核放大 3 倍。

**建议的判别方法（canary）：** 在某一批的 lane payload 中混入少量构造缺陷条目（取自
历史 confirmed 缺陷的同型变体），检验表层筛查是否检出。需要注意：构造条目不属于 catalog
条目，不能进入 `selected`、`results.jsonl` 或队列状态，只能作为一次性诊断，其派生产物
写入被忽略的 `.artifacts/`，且必须在批次记录中说明该批 payload 含诊断条目。这项改动会
触及审核输入构造方式，属于跨批次策略，需要维护者批准。

---

## 8. 观察七：一类可确定性判定的缺陷仍在走 LLM 审核

历史 confirmed 裁决中，相当一部分属于格式类，可由字符串规则客观判定，例如：

- `译文首字前多出空格，且……缺少原文对应的空行`
- `中文句末使用半角感叹号，格式不一致`
- `第一句使用半角逗号并前后加空格「通道 , 传送到」……属标点格式破坏`
- `target 中两个 %d 仍按"伤害、半径"排列，但 args_order=[2,1] 会将参数互换`

而 `tools/i18nlib/lint.py` 目前只有两个 code：`format-mismatch` 与
`format-shape-difference`，覆盖 format token，不覆盖标点体系、首尾空白与换行计数。

对全量 29,828 条运行附录的正则扫描（耗时 <1 秒），在**未审的 27,602 条**中命中 1,521 条
（5.5%）：

| 模式 | 命中 | 示例 |
| --- | ---: | --- |
| 半角标点紧邻中文 | 735 | `%s 抵抗传送!` |
| 换行计数与原文不符 | 406 | — |
| 原文无、译文有的首尾空白 | 339 | ` 我建议你不要从雪巨人的……` |
| 句末语气标点丢失（`!`/`?` → `。`） | 119 | `Survived the Fearscape!` → `在恶魔空间幸存下来。` |

按组件分布：tome 1,105/19,914（5.5%）、orcs 191/3,663（5.2%）、cults 119/1,933（6.2%）、
ashes-urhrok 71/837（8.5%）、engine 28/991（2.8%）、boot 7/264（2.7%）。

**结论：** 这类判据的正确归属是确定性门禁而非 LLM 审核。lint 一次运行即覆盖全语料，
而表层审核要以 122 条/小时的速度走 227 小时才能到达同样的覆盖面。把这一层前移，既提高
覆盖速度，也让表层筛查的注意力集中在真正需要语义判断的部分。

**必须注意的限制：** 这 1,521 条是候选，不是缺陷。抽样可见明显的潜在误报，例如
`generic acid retribution` → `通用 酸性反击伤害` 的空格可能是刻意的词间分隔；换行计数
差异可能是合理的排版调整。落地前需要先在一个已审样本上标定每条规则的误报率，只把误报
率足够低的规则设为 error，其余设为 warning 或仅作为选片信号。新增 lint 规则会影响全部
条目并可能改变既有译文，属于跨批次策略决定，需要维护者批准。

---

## 9. 观察八：已 OK 条目中存在同型未判定模式

在恢复后判为 OK 的 887 条中，有 **11 条**带有早期已被 confirmed 的同型模式：

| 类型 | 条数 | 实例 |
| --- | ---: | --- |
| 句末语气标点丢失 | 8 | `%s is knocked back!` → `%s 被击退。`（4 次）；`Not enough space to summon!` → `没有足够的空间召唤。`（4 次） |
| 半角标点紧邻中文 | 3 | `You cannot move!` → `你无法移动!`；`#CRIMSON#%s shatters %s shield!` → `……粉碎了%s的护盾!` |

同一扫描在全部 2,179 条历史 OK 条目上命中 33 条（1.5%），在 47 条 ISSUE 条目上命中 5 条
（10.6%）。

**问题的性质不是漏审，而是缺少统一判据。** 早期批次将"中文句末使用半角感叹号"判为
confirmed 缺陷，近期批次对同一模式判 OK。在没有成文规则的情况下，两种判断都不能说是
错的，但它们不能同时成立——这正是 AGENTS.md 要求交回维护者的"确立跨批次统一策略"。

在这条规则定下来之前，观察七的 lint 规则无法落地（不知道该把什么设为 error），而已完成的
2,226 条的判定一致性也无法主张。因此这是所有改进项中**唯一的前置阻塞项**。

---

## 10. 观察九：剩余工作中约 16% 是完全重复文本

对未审的 27,602 条按 `(source, target)` 精确配对去重：

- 唯一配对 24,137 个，**3,465 条（12.6%）为组内重复**；
- 另有 **1,006 条**的配对与已审条目完全一致；
- 合计约 4,471 条（16.2%）为完全重复文本。

重复度最高的配对：`void`→`虚空`（14 次）、`floor`→`地板`（13 次）、
`Sorry, I have to go!`→`抱歉，我要走了！`（12 次）、`acid`→`酸性`（10 次）。

这一模式在历史裁决中已经出现过：`entity type 的 elemental 被译为"元素"` 这条 observation
以逐字相同的措辞出现了 4 次，`Tanner` 误译出现 3 次——同一判断被重复生产了多次。

**不能直接跳过重复条目。** AGENTS.md 明确规定"同一个英文词在不同 section 或 `source_tag`
下可以有不同译法"，`logical_entry_identity` 在这 27,602 条中两两互异也说明它们是不同的
逻辑条目。正确做法是**分组呈现而非跳过**：把同配对条目合并为一个审核项，附上全部出现
语境清单，由 reviewer 一次性判断"该译法在所有列出语境下是否都成立"，结果再展开回各条
`entry_revision_identity`。守恒证明与逐条结果记录都保持不变。

由于成本几乎全在每批固定开销上（观察一），去重的收益不是"省下 reviewer 时间"，而是
**提高每批的有效覆盖**——在同样的 80 条上限下覆盖更多条目。这使它与批量上限提升是
互补而非替代关系。

---

## 11. 建议与优先级

| # | 建议 | 收益 | 需要授权 |
| ---: | --- | --- | --- |
| 1 | 停止按 `fixed_source_identity` 切批，按上限装箱，由 adapter 分 run | -35% 批次 | 否（既定顺序内的批次边界选择） |
| 2 | 压缩交接文档为"当前状态 + 指针"，历史小节归档 | 回收 +50% 漂移 | 否（纯文档） |
| 3 | 确立中文标点体系判据（半角标点、句末语气标点） | 解除 #4 阻塞 | **是**（跨批次策略） |
| 4 | 按 #3 的判据扩充 lint 规则，先标定误报率再设级别 | 一次覆盖全语料 | **是**（影响全部条目） |
| 5 | canary 灵敏度校验 | 区分 H1/H2 | **是**（改动审核输入构造） |
| 6 | 重构优先键，用机械信号替代已退化的 risk rank | 恢复排序信息量 | **是**（改 `policy-v1.json`，批次边界生效） |
| 7 | 提升批量上限 80 → 更高 | 与倍数成正比 | **是**（§14.2 升级提案） |
| 8 | 按 `(source, target)` 分组呈现重复条目 | +16% 有效覆盖 | **是**（改动 payload 构造） |

**关于 #7 的升级证据。** 方案 §14.2 要求升级必须有可核验触发证据，其中一条是"pilot/连续
批次证明 80 条或单 active batch 是主要瓶颈，且人工裁决/修复没有积压"。当前数据同时满足
两个分句：固定开销 22–29 分钟对门禁 82 秒（观察一、二）证明批次数量是瓶颈；20 批 887 条
零 observation、零修复、R=0（观察六）证明没有裁决积压。§14.2 同时规定"即使触发，也只批准
解决该证据的最小下一机制"——因此提案应当只申请提高 `MAX_BATCH`，不附带多 writer、并行
active batch 或新 consumer schema。

**建议的执行顺序。** #1 与 #2 可立即执行且不需要授权，应先做，同时它们也为后续项提供
更干净的基线。#3 是 #4 的前置，也是唯一阻塞项，应尽早决定。#5 应当在 #7 之前完成——在
未验证筛查灵敏度的前提下扩容会放大风险。#6 与 #8 可在 #4 落地后一并提案，因为机械扫描
的信号同时服务于这两项。

**影响估算（剩余 27,602 条）：**

| 情形 | 每批条数 | 批次数 | 估算工时 |
| --- | ---: | ---: | ---: |
| 现状 | 44（实测均值） | 627 | 227 h |
| 落实 #1 + #2 | 80 | 345 | 127 h |
| 再落实 #8 | 80（有效 ~93） | 297 | 109 h |
| 再落实 #7（上限 240） | 240 | 116 | 43–81 h（见下方修正） |

工时按每批 22 分钟估算；#2 若成立则实际单批成本还会低于此值。这些是量级估算，不是承诺。

> **修正（起草升级提案时发现）。** 上表第 4 行最初记为 42 h，该估算偏乐观：它只考虑了
> `MAX_BATCH = 80`，遗漏了 `translation_surface_screen_v1` 契约对**单次 screen** 的 80 条
> 上限。剩余语料只有 4 个不同的 `fixed_source_identity`（其中一个覆盖 21,169 条），因此
> 上限一旦超过 80，99% 的批次都会产生超过 80 条的同质 run，而生产批次路径不能使用
> carry-over（它与 §266 的 selected 守恒冲突）。单独提高 `MAX_BATCH` 因此收益有限。
> 完整分析、最小机制与分阶段验证方案见
> [批量上限升级提案](production-review-batch-limit-upgrade-proposal-v1.md) §2–§5。
> 这一发现不影响 #1（按 80 装箱）——实测显示 cap80 下不产生任何超过 80 条的 run。

---

## 12. 风险与反对意见

- **本文的收益估算全部基于"每批固定开销恒定"这一假设。** 若批量提升后每批开销随条数
  上升（例如逐条固定源码核验的时间开始显现），#7 的收益会低于线性外推。观察一的
  `r=0.10` 只在 2–80 条区间内成立，不能外推到 240 条。提案应包含一次 160 条的中间验证。
- **机械扫描的误报率完全未标定。** 1,521 条候选中有多少是真缺陷目前未知，抽样可见明显
  的潜在误报。在标定之前，任何"发现了 1,521 个缺陷"的表述都是错误的。
- **观察五（优先键退化）本身不是缺陷。** 在需要 100% 覆盖的任务里，排序只影响收益的时间
  分布，不影响总量。#6 的价值在于早期发现问题、而非减少总工作量；若维护者的目标就是
  全量覆盖，#6 的优先级应当低于 #1、#7。
- **观察四的归因未经实验证实**，压缩文档后需要观察后续批次的周期是否回落。
- **#5 canary 有成本，且会在批次记录中留下需要额外说明的诊断条目**；若维护者认为
  H1 解释已足够，可以选择跳过，但那样就应当在 #7 提案中明确记录"未验证灵敏度"这一
  已知风险，而不是默认它不存在。
- 本文未考察 contextual（深审）路径：D 长期停在 47，恢复后 20 批未产生任何深审。若后续
  策略要提高 deep 抽检比例（方案 §15 列为待定参数），本文的成本模型需要重算。

---

## 附录 A：复现脚本

以下脚本均为只读，在仓库根目录运行，不写入任何文件。

**A.1 批次规模、周期与门禁耗时**

```python
import json, glob, datetime as dt
p = lambda s: dt.datetime.fromisoformat(s)
rows = []
for f in sorted(glob.glob('evidence/production-review-v2-lite/batches/*/gates.json')):
    b = f.split('/')[-2]; r = json.load(open(f)).get('result', {})
    if 'started_at' not in r: continue          # schema 1 无逐项时间戳
    n = sum(1 for _ in open(f'evidence/production-review-v2-lite/batches/{b}/results.jsonl'))
    rows.append((p(r['started_at']), b, n,
                 (p(r['finished_at']) - p(r['started_at'])).total_seconds()))
rows.sort()
for i, (st, b, n, g) in enumerate(rows):
    cyc = (st - rows[i-1][0]).total_seconds()/60 if i else 0
    print(f'{b:22} n={n:3d} gate={g:5.0f}s cycle={cyc:5.1f}min')
```

**A.2 ISSUE 产出率与裁决数**

```python
import json, glob
rows = []
for d in sorted(glob.glob('evidence/production-review-v2-lite/batches/*')):
    res = [json.loads(l) for l in open(d + '/results.jsonl')]
    rows.append((json.load(open(d + '/manifest.json'))['recorded_at'], d.split('/')[-1],
                 len(res), sum(1 for r in res if r['surface_verdict'] == 'ISSUE'),
                 sum(1 for _ in open(d + '/adjudications.jsonl'))))
for row in sorted(rows):                        # 按 recorded_at 排序
    print('%s %-22s n=%3d ISSUE=%3d adj=%3d' % row)
```

**A.3 机械模式扫描（产出候选，非缺陷）**

```python
import json, re, glob, collections
cat = [json.loads(l) for l in open('evidence/production-review-v2-lite/catalog/entries.jsonl')]
seen = set()
for d in glob.glob('evidence/production-review-v2-lite/batches/*'):
    for l in open(d + '/results.jsonl'):
        seen.add(json.loads(l)['entry_revision_identity'])

def flags(o):
    s, t, f = o['source'], o['target'], []
    if re.search(r'[一-鿿][,;:!?]', t) or re.search(r'[,;:!?][一-鿿]', t):
        f.append('halfwidth-punct-next-to-cjk')
    if t != t.strip() and s == s.strip():
        f.append('stray-leading-trailing-space')
    if s.count('\\n') != t.count('\\n') or s.count('\n') != t.count('\n'):
        f.append('newline-count-mismatch')
    if s.rstrip()[-1:] in '!?' and t.rstrip()[-1:] not in '！？!?':
        f.append('terminal-punct-tone-drop')
    return f

c = collections.Counter()
for o in cat:
    if o['entry_revision_identity'] in seen: continue
    hits = flags(o)
    if hits: c['ANY'] += 1
    for x in hits: c[x] += 1
print(c)
```

**A.4 优先键退化与重复度**

```python
import json, glob, collections
cat = [json.loads(l) for l in open('evidence/production-review-v2-lite/catalog/entries.jsonl')]
seen = set()
for d in glob.glob('evidence/production-review-v2-lite/batches/*'):
    for l in open(d + '/results.jsonl'):
        seen.add(json.loads(l)['entry_revision_identity'])
unrev = [o for o in cat if o['entry_revision_identity'] not in seen]
hi = [o for o in cat if o['risk']['has_args_order'] or o['risk']['has_special']]
print('rank-1 总数', len(hi), '未审', sum(1 for o in hi if o['entry_revision_identity'] not in seen))
print('group_size 分布', collections.Counter(o['risk']['component_group_size'] for o in unrev).most_common(3))
pairs = collections.Counter((o['source'], o['target']) for o in unrev)
print('未审', len(unrev), '唯一配对', len(pairs), '组内重复', len(unrev) - len(pairs))
okpairs = {(o['source'], o['target']) for o in cat if o['entry_revision_identity'] in seen}
print('与已审配对相同', sum(1 for o in unrev if (o['source'], o['target']) in okpairs))
```

---

## 附录 B：相关文档

- [正式审核方案](translation-production-review-v2-lite-plan.md)——§5 优先键、§266 run 分组、
  §14.2 升级触发、§15 待定参数。
- [当前交接](production-review-handoff-2026-09-05.md)——恢复基线与逐批记录（见观察四）。
- [代理操作与门禁手册](agent-workflow.md)——连续批次循环与门禁。
- [AGENTS.md](../AGENTS.md)——停下条件、跨批次策略决定、校对判定依据。
- [中文标点判据提案 v1](translation-punctuation-convention-proposal-v1.md)——本文 §9 与
  §11 第 3、4 项的落地草案（待批准）。
- [批量上限升级提案 v1](production-review-batch-limit-upgrade-proposal-v1.md)——本文 §11
  第 7 项的 §14.2 升级申请，并修正本文对上限收益的估算（待批准）。
