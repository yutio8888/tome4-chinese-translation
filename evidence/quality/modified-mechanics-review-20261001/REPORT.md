# 已修改机制译文专项复核报告

只读检查完成，相关机制仍有待确认项。完成时间：2026-10-02T05:17:32.497839+00:00。本报告不表示译文全部正常，也不计入生产 done/deep_reviewed。

比较 BASE `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00` 至 TARGET `bfde8c53d50b065837ff34dc08639f7dbc5816f5`；冻结工作集 SHA-256 `6526c22d7a785ff92b7bd64028a93a2602e93c0bc697dc268639a6ba988925df`。规范译文与 TARGET blob、版本 manifest 在最终验收时仍一致。[范围与授权](SCOPE.md)、[输入身份](input-manifest.json)、[验收记录](acceptance.json)。

## 覆盖与检查

| 项目 | 完成口径 |
| --- | --- |
| 净差异对账 | 1621 条：969 mechanics、129 mixed、523 excluded；无未分类候选 |
| 改动分类 | 1307 semantic、310 format_only、4 structural（含 excluded） |
| 入选语义／结构 | 788 条全部完成整句英中、旧新与独立复核 |
| 独立复核 | 828 条有效结果：首包 10 条及后续 84 包；含排版样本，不能等同源码通过数 |
| 结构检查 | 1621 条全部有记录；310 条 format_only 全量证明；严格 lint 30308 条，0 错误、0 警告 |
| 必须源码核验的集合 | 1065 条全部记录：1057 条 host_source_checked，8 条 source_unavailable/pending |
| 宿主全部源码记录 | 1070 条：1062 条 checked、8 条 pending；额外 5 条不充抵必查集合 |
| 排版／动态展示 | 40 条、80 次代表参数重渲染；39 条数字与中文片段边界通过，1 条 Possessors 消费者待确认 |
| 生命周期 | 85 task 闭合 DONE 且完成验证；96 dispatch 全部确认归档；11 次无效运行不计有效覆盖 |

[逐条覆盖账](coverage.jsonl)保存稳定身份和 occurrence；[工作集](workset.json)保存完整旧新文及分类／排除理由；[结构记录](structural-checks.jsonl)、[源码结论](source-checks.jsonl)和[源码锚点](source-anchors.jsonl)分别保留结构、计算／消费者及固定源码证据。抽样按冻结身份哈希排序，名单见 [sampling.json](sampling.json)。抽样发现机制问题后，本体与 Orcs 排版层扩查，必查集合升级至 1065 条，见 [扩查记录](sampling-expansions.json)。

## 裁决结果

共 209 个 claim：**169 confirmed、8 pending、32 advisory**。分别涉及 166、8、32 条不同译文；这些条目集合可能重叠，不能相加成错误条目数。一个译文可能同时有新增问题和上游差异。详见 [问题账](findings.jsonl)；每项保留 revision、位置、旧新文、影响、最强反证、锚点与宿主裁决。

| 归因（claim 数） | confirmed | pending | advisory |
| --- | --- | --- | --- |
| 上游英文／实现差异 | 132 | 0 | 11 |
| 既有授权／撤销观察 | 0 | 0 | 3 |
| 既有译文问题／歧义 | 27 | 0 | 14 |
| 本轮新增／新增歧义 | 10 | 0 | 4 |
| 证据缺口 | 0 | 8 | 0 |

上游英文／实现差异是在本次固定本体或 DLC 快照中确认的差异，不能直接算作汉化新增错误，也不能推导其他发行版本同样存在。advisory 中包含已撤销的 reviewer 观察，保留理由，不计有效错译。

### 本轮新增的 confirmed 修复候选

| finding | 译文位置 | 问题 |
| --- | --- | --- |
| MMR-005 | `tome-orcs.lua:1589` | 新增以目标为中心错误；实际为射手起点朝目标方向的半径4锥形。 |
| MMR-007 | `tome-orcs.lua:1606` | 武器字段physcrit设100不能直接证明下一次攻击实际物理暴击率100%；固定弓术消费者传的是ammo。 |
| MMR-010 | `tome-orcs.lua:5627` | 本轮新增法力限定，实际燃烧四种奥术资源。 |
| MMR-017 | `mod-tome.lua:9859` | 恢复类词缀restorative从疗愈改成振奋，与healing_factor/life_regen核心效果语义不符。 |
| MMR-018 | `mod-tome.lua:9974` | 恢复类词缀restorative从疗愈改成振奋，与healing_factor/life_regen核心效果语义不符。 |
| MMR-026 | `mod-tome.lua:7049` | draining physical 改成生命汲取，丢失物理伤害类型限定。 |
| MMR-027 | `tome-ashes-urhrok.lua:176` | magic stat 从魔力值改为魔法属性，属性术语从明确魔力退回泛魔法。 |
| MMR-033 | `tome-orcs.lua:8158` | 询问学习tinkers crafting的奖励被改成“插件制作”；指蒸汽工具装备制作的对象身份丢失。 |
| MMR050 | `mod-tome.lua:28421` | 新增“每个负面效果持续1回合”将时长绑定到已有负面效果；实际按负面效果数量计算本技能减速持续时间，不改已有负面效果时长。 |
| MMR053 | `tome-cults.lua:3197` | 新增“目标两侧的敌人”，而消费者util.coordAddDir以self.x/self.y为中心选两侧格；并非目标格两侧。 |

后续应先集中核对会改变操作决策的条件、范围、对象及数值关系，再处理明确术语与失义。上游差异须分别决定是否让中文遵从固定实现、是否提交上游，以及目标发行版本，不能直接批量替换。现有译文问题单列，避免把它们归为本轮回归；本报告未应用任何修复。

## 待确认与限制

8 条 Possessors（译文行 5、56、119、146、152、270、317、356）已完成表面语义与结构检查，缺少可核验公开源码映射／版本／快照，附身、身体、成就与消费者行为保留 pending。最小后续动作是补来源身份并冻结对应实现，再只补查这些条目。展示中的 Possessors 数字消费者也未记通过。

本体／引擎证据绑定 manifest commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`，没有用另一版本工作树替代。三个官方 DLC 的仓库、commit、发行版本未固定；文件 SHA-256 只绑定本次证据。待运行验证的合成效果、回合结算与动态属性问题保留 advisory，不将代码局部推断提升为实测。

展示使用 LuaJIT string.format 和固定引擎 toTString/tokenize，代表参数不是实际游戏属性。**未实际运行游戏**；边界检查不证明完整界面、升级预览或全部合法参数均通过。

## 编排与交付

独立 reviewer 使用 Paseo contextual v2 review_only；原生结果、冻结输入、身份、只读审计和状态证据位于 [首包](completed-trial/)及[后续包](completed-packages/)。首次外发拒绝和第 62 包软归档拒绝均在明确用户授权后解决；历史 WAIT_USER 快照不代表当前状态。cwd、JSON 契约或当时只读边界不合格的运行保留原证据，归档后 fresh retry，不计覆盖。用户随后允许临时文件的授权不追溯改变拒收记录。

本次仅写专项编排和证据；未改译文、术语库、生产 catalog／queue／ledger，未提交、push 或发布，既有用户文件保持原状。任务按方案第八节只读验收闭合；保留 pending 不要求问题清零。后续修复与术语／跨批策略须作为独立授权范围处理。
