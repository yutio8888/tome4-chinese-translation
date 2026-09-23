# 术语范围与审核判定规则校准落实

日期：2026-09-23。依据用户“请执行”的授权，完成三条术语范围调整、审核规则维护和受影响译文复核。本次为有界规则维护；没有续开实验样本，没有修改译文，也不宣称生产 `DONE_VERIFIED`。

## 已落实的规则

`terminology/combat.tsv` 仅改变以下三行的 scope，均由 `core` 改为 `global`，其他字段不变：

| 行 | source | source_tag | target |
| --- | --- | --- | --- |
| 135 | global speed | _t | 全局速度 |
| 136 | global speed | tformat | 全局速度 |
| 140 | Physical Power | tformat | 物理强度 |

依据为已审查的[范围提案及源码锚点](../all-modified-review-20260922/experiments/calibrated-pilot40-20260923/SCOPE-AUDIT.md)。大小写、标签和具体语境仍须匹配；没有扩大其他 core 行。DLC 证据为哈希固定快照，源码仓库、commit 与目标版本映射未固定。

`TERMINOLOGY.md` 明确 scope 是适用范围而非发现来源，要求逐行有证据地扩大范围并重新冻结后续复核输入。`docs/agent-workflow.md` 增加以下判定口径：

- 正确性与修复优先级分开；低影响不等于无错，高影响不等于已证实。
- 确认前检查最强上下文反证，保留完整句段、主体承接和消费逻辑。
- 用户定标的三类表达只记澄清建议，不计确认错译；不泛化到其他语境。
- 长文本共同未报错项仍检查主体、数量、时间、条件和因果。
- 模型共识不作真值，一轮小样本不作模型淘汰依据。

这些是新输入及主代理裁决的规则，没有新增 reviewer 输出字段、改变角色权限或扩展修复轮次。旧实验输入、报告及统计保持原样。

## 受影响译文

使用工具配置的 LuaJIT 加载全部 11 个组件、30,308 条译文。以三条术语的大小写、词边界和 exact source_tag 筛选新增 DLC 适用项，再逐项核对完整原译文：共 22 条，其中 9 条已使用“物理强度”，13 条仍使用“整体速度”。结论仅针对这三个术语，不表示对整条译文作了全量验收。

| 当前文件及行 | 旧修改清单 ID（若有） | 本次结论 |
| --- | --- | --- |
| tome-cults.lua:3107 | entry-03600 | 新范围下需统一为全局速度 |
| tome-cults.lua:3120 | entry-03602 | 新范围下需统一为全局速度 |
| tome-cults.lua:3200 | entry-03605 | 物理强度符合 |
| tome-cults.lua:3329 | — | 物理强度符合 |
| tome-cults.lua:3395 | entry-03620 | 新范围下需统一为全局速度 |
| tome-cults.lua:3530 | entry-03633 | 新范围下需统一为全局速度 |
| tome-cults.lua:3860 | — | 新范围下需统一为全局速度 |
| tome-orcs.lua:2012 | entry-03844 | 新范围下需统一为全局速度；仅叙事引用 |
| tome-orcs.lua:4036 | — | 物理强度符合 |
| tome-orcs.lua:4381 | — | 新范围下需统一为全局速度 |
| tome-orcs.lua:4781 | — | 物理强度符合 |
| tome-orcs.lua:4892 | — | 新范围下需统一为全局速度 |
| tome-orcs.lua:5023 | entry-03927 | 物理强度符合 |
| tome-orcs.lua:5060 | entry-03930 | 物理强度符合 |
| tome-orcs.lua:5296 | — | 新范围下需统一为全局速度 |
| tome-orcs.lua:5330 | entry-03948 | 物理强度符合 |
| tome-orcs.lua:5649 | entry-03973 | 新范围下需统一为全局速度 |
| tome-orcs.lua:5708 | — | 物理强度符合 |
| tome-orcs.lua:5752 | — | 新范围下需统一为全局速度 |
| tome-orcs.lua:5870 | — | 物理强度符合 |
| tome-orcs.lua:6207 | — | 新范围下需统一为全局速度 |
| tome-orcs.lua:6485 | — | 新范围下需统一为全局速度 |

旧清单之外的 12 条没有借用或新造 entry-ID，以本报告的 SR 编号及文件哈希定位。完整原译、section、反证、优先级和后续动作见 [AFFECTED.json](AFFECTED.json)。13 条术语一致性修复已形成有界清单，译文尚未修改；后续生产修复需使用新冻结工作集，不能据新 scope 倒改旧审核统计。

## 验证结果与限制

- `python3 -B tools/i18n doctor`：通过；DLC 来源未固定的既有提示保留。
- `python3 -B tools/i18n lint --strict`：30,308 条，零错误、零警告。
- 静态术语审计：722 行、零阻断、16 项建议；finding 与修改前完全一致，scope 统计按三行调整。
- 动态术语审计：71 未使用、2 不一致、5 候选、35 多译；原有两项不一致仍为 Air／空气量、draining physical／物理汲取。差异只涉及三条术语记录的 scope 元数据。
- 领域审计：零未映射、6 项既有建议，报告与修改前一致。
- `python3 -B tools/paseo_contract_check.py`：10 份活跃文档、4 个版本、16 项声明通过；另已人工核对新增规则不改变角色、输出 schema 和收敛边界。
- 所有 11 个译文文件和原有 2,061 个实验文件哈希未变。三条术语的 scope 是术语库唯一数据变化。

动态术语审计的上述不一致统计使用完整 source 精确匹配，不覆盖嵌在长文本中的全部术语短语，因此不能把“审计未新增不一致”解释为这 13 条译文已符合新规范。本次独立的有界扫描与语境复核补足了这一覆盖缺口。

核验记录见 [VERIFICATION.json](VERIFICATION.json)。派生审计和修改前对照保存在忽略目录 `.artifacts/i18n/scope-rule-calibration-20260923/`。本次只改规则和术语范围，不涉及运行时代码或打包内容，未运行构建或全套工具测试。
