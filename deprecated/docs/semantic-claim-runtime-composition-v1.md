# 机制 claim 与运行时组合 registry v1

本规范定义 Phase 0–2 的最小确定性防线。规范 registry 是
`evidence/quality/semantic-claim-regressions-v1.json`，统一入口为：

```bash
python3 -B tools/i18n claims check \
  --registry evidence/quality/semantic-claim-regressions-v1.json \
  --strict
```

成功时退出 0，并报告 numeric claim、anchors-only briefing、runtime composition 和
pending 数量；JSON、schema、路径、绑定、算术、重渲染或 assertion 失败时退出 5。`--strict`
是 CI 的规范调用形式；校验器在非 strict 模式也不会放宽 exact schema。它不调用 provider，
不修改 registry，也不扫描或改写 Lua。

## Phase 0 定界

枚举只采用冻结方案已经要求、且本批源码样本能支持的维度：

- `quantity_kind`：`damage`、`heal`、`shield`、`duration`、`count`、`percent`、
  `radius`、`other_numeric`、`unknown`；无法可靠分类时必须用 `unknown`。
- `scope`：`on_apply`、`per_tick`、`total_over_effect`、`on_expire`、`unknown`。
- 固定组成阶段：`on_apply`、`periodic_tick`、`on_expire`；其他阶段用 `unknown`
  decomposition，不扩展猜测枚举。
- `duration_turns` 与 `tick_count` 是两个独立字段。未知值写字符串 `unknown`，不能从一者
  推导另一者。无 periodic component 的纯即时／到期组成必须使用 `tick_count=0`；纯即时允许且
  要求 `duration_turns=0`，到期或 periodic 组成仍要求正 duration。
- runtime `surface_shape`：`bare_noun`、`possessive_phrase`、`pronoun`、
  `pre_punctuated_clause`、`tagged_fragment`、`unknown`。

固定 engine commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的有限样本证明了本批需要的
即时与 periodic 分量：`game/modules/tome/data/talents/spells/fire.lua` 的 `Flame.info/action`
把技能伤害送入 `game/modules/tome/data/damage_types.lua` 的
`DamageType.FIREBURN.projector`；projector 默认立即结算输入的 `1/2`，剩余 `1/2` 分 3 tick，
所以输入是整个效果的总量角色。该固定分解的 `applicability=effect_absent`：已有 BURNING 时，
`EFF_BURNING.on_merge` 会合并旧、新剩余总伤害并重算 duration 与每 tick power；随后
`EFF_BURNING.on_timeout` 才消费 `eff.power`。因此总伤害仍被保存，但重施后的 tick 分布不是无条件
固定三次。治疗、护盾及其他变量形态本批不固化；证据不足时 decomposition、applicability 和
scope 必须为 `unknown`。

Startling Shot 的实际调用点位于公开 Orcs DLC 的
`tome-orcs/data/talents/steam/gunslinging.lua:114-115`，调用 `%s misses %s shot.` 时依次传入
`srcname` 和 `string.his_her(self)`。固定 engine helper 的英文分支为 `his`／`her`／`its`；当前
translation HEAD `8c9b065601c4545d9f19e6983bb2c5088561be10` 的 engine locale domain
`engine.lua:1407-1409` 分别映射为“她”／“它的”／“他的”，其中“她”是裸代词，三者不能假设为
统一所有格短语。Orcs locale 在 `tome-orcs.lua:2959-2960` 仅重复 `his`／`her`，没有 `its`；这些
重复值不用于推断或声明 locale 加载优先级。`srcname` 必须覆盖动态的可见姓名（不虚构 locale row）
与不可见时 `_t"Something"` 经 `tome-orcs.lua:5104` 映射为“某物”的两个表面分支。
manifest 只固定 Orcs 提取快照，不固定 DLC 源码仓库、commit 或版本，因此调用点记录必须是
`source_pinned=false`、`status=pending`；本机观察到的公开源码只能冻结回归样例，不能冒充
manifest 固定源码。`runtime_compositions[0].target_template` 是裁决后的、尚未落地的修正案；
当前生产 `tome-orcs.lua:5105` 仍为
`t("%s misses %s shot.", "%s的%s射击打偏了", "logSeen")`。该 composition 只有在 DLC required
source 已固定且生产 target 已与冻结模板一致时，才能转为 `confirmed`。registry 和本文只使用
逻辑源码路径，不记录本机绝对路径。

## Exact schema

顶层必须且只能有：

```text
schema_version, registry_id, numeric_claims,
reviewer_briefings, runtime_compositions
```

所有对象拒绝 extra key 和缺失 key；所有 ID 在三类记录之间全局唯一；JSON 对象重复键也被
拒绝。源码路径必须是无 `.`、`..`、反斜线或绝对前缀的相对 POSIX 路径。

### Numeric claim

每条记录必须且只能有：

```text
claim_id, status, string_key, source_text, target_text,
placeholder_index, placeholder_token, args_order, quantity_kind,
source_explicitness, target_explicitness, scope, explicitation_justified,
anchors, decomposition, target_assertions
```

`placeholder_index` 从 1 开始，始终按 source 顺序解析到 `source_text` 中的
`placeholder_token`。`args_order` 必须为 `null` 或 source placeholder index 的完整排列；校验器按
该排列要求 target 保留全部 raw token，允许 `[2,1]` 这类合法译文重排，但不允许遗漏、精度漂移或
重复 index。每个 anchor
必须且只能有 `component`、`revision`、`source_pinned`、`path`、`symbol`、`line_hint`、
`placeholder_expression`、`binding_reason`、`required`。至少一个 anchor 为 required；任何
required anchor 未固定时，记录不得标为 `confirmed`。revision、symbol 与 placeholder binding
均不得为空。`line_hint` 指向同一 anchor 的 `placeholder_expression` 或实际消费表达式所在行，
只是人工核验提示；validator 不读取外部源码 checkout，也不声称在 CI 中验证行号。

`source_explicitness` 与 `target_explicitness` 采用有序关系
`ambiguous_scope < explicit_scope`。target 比 source 更明确时必须
`explicitation_justified=true`，且只有非 pending、所有 required anchor 均固定时才允许；target
没有增加明确度时该布尔值必须为 false。该关系是机械约束，不依赖“每回合”等关键词猜测。

`decomposition.kind=fixed_fraction` 时，必须用 `applicability` 结构化声明
`effect_absent`／`unconditional`／`unknown`；每个 component 使用约分后的
`{numerator, denominator}`、明确 `phase` 和正整数 `count`。校验器机械计算
`fraction × count` 之和，核对 `total_fraction_of_input`，并要求 periodic component 的 count
之和等于独立的 `tick_count`；没有 periodic component 时 tick count 必须为 0。
`total_over_effect` 的组成总和必须恰为 1。未知机制只允许 `kind=unknown`、空 components、unknown
duration/tick/total/applicability 和 `scope=unknown`；不得使用自由文本 `runtime_formula`。

`target_assertions` 是经源码裁决后冻结的完整 target required/forbidden 片段。它用于回归已知
claim，不是通用关键词判案器。诸如“每回合、总计、立即”的全仓扫描只能生成候选，不能成为
本规范新增的硬门禁。

### Anchors-only reviewer briefing

briefing 必须且只能包含：

```text
briefing_id, string_key, source_text, candidate_target,
placeholder_index, placeholder_token, args_order, anchors, read_budget
```

briefing 的 `args_order` 采用与 numeric claim 相同的 null-or-permutation 规则，并机械要求
`candidate_target` 对 source raw token 完整保序或按声明重排；`placeholder_index` 仍绑定 source
顺序。`read_budget` 只含正整数 `max_lines_per_anchor` 和非负整数 `max_dependency_hops`。exact schema
明确排除 `scope`、`components`、`tick_count`、`total`、期待 verdict 或其他预填结论。校验器只
保证 briefing 结构独立；单次模型是否被诱导属于周期性 eval，不是 CI gate。

### Runtime composition

composition 必须且只能包含：

```text
case_id, status, string_key, source_template, target_template,
args_order, placeholders, renderings
```

每个 placeholder 记录 `index`、真实 `runtime_source` 与非空 `variants`。每个 variant 必须且只能有
`variant_id`、`surface_shape`、`sample_value` 和非空 `anchors` 数组；数组复用统一 anchor exact
schema，且每个 variant 至少一个 anchor 为 required。call-site、helper branch 与 locale mapping
必须按适用性分别成行，不能塞进一个 free-text anchor；任何 confirmed composition 的 required
anchor 未固定时都失败。`renderings` 为每个 placeholder 选择一个
variant ID，冻结完整 `rendered_sentence` 及其 required/forbidden assertions；校验器要求 renderings
完整覆盖所有 placeholder variant 的笛卡尔积，不能漏掉隐藏姓名、女性或中性分支。

index 必须恰好覆盖 source template 的全部 printf 参数；target 参数数必须相等；`args_order` 为
`null` 或完整排列。numeric claim、briefing 与 composition 都复用 `lint.extract_format_tokens()`；
composition 还会逐个扫描 source/target template 的每个百分号，要求它只能开始 `%%` 或一个完整
Lua 5.1 scanformat token。因此 `%r`、`%a`、`%*s` 与末尾孤立 `%` 都 fail closed，而不会被静默
跳过；校验器比较包含 flags、width 与 precision 的完整 raw token。composition 在应用
`args_order` 后比较 raw token，再按实际顺序把每组样例值代入整个
target template，结果必须逐字等于冻结完整句。因此 `%0.2f → %f` 漂移、错序、遗漏 variant、重复
“的他的”或只验证模板局部都会失败。

composition 的 canonical format token 先服从 Lua 5.1 `scanformat` 语法边界：flag 字符最多 5 个，
width 最多 2 位，precision 最多 2 位。长度不超界的重复 flag 合法；例如 `%10q` 与 `%--q` 均可
通过，而 `%100q`、`%.100q` 和 6 个 flag 会 fail closed。runtime composition v1 的 `s`
conversion 只接受没有 flags、width 或 precision 的原始裸 `%s`；LuaJIT 按 UTF-8 byte 计算这些
modifier，而 Python 按 Unicode character 计算，因此不把带 modifier 的 `%s` 纳入 v1。

语法通过后，`%q` 重渲染只覆盖已与 manifest 要求的 LuaJIT 验证一致的安全子集：sample 必须是
非空 string，且不得包含除 LF 外的 C0（U+0000..U+001F）或 DEL（U+007F）。CR、NUL、TAB、其他
C0 与 DEL 一律 fail closed；结果使用双引号包围，反斜杠与双引号加反斜杠，LF 写成反斜杠加
实际换行。`%q` 继续忽略已经通过上述长度检查的 flags、width 与 precision，校验器保持这些 raw
token 逐字比较并在渲染时采用相同行为。runtime composition v1 对 source 与 target template
都只允许上述裸 `%s` 和 `%q` conversion；所有 numeric
conversion 均 fail closed，不能由 Python `%` 代替 Lua numeric formatting。数值机制证据继续由
numeric claim 与结构化 decomposition 记录；若未来需要数值 runtime composition，必须另立版本化
schema 和 renderer。所有 `sample_value` 都在 exact-schema 字段边界要求 non-empty string；
`%%`、`args_order` 与完整 variant 笛卡尔积仍按上述规则处理。

## 保守默认与复用边界

没有 accepted directional anchor、required anchor 未固定或 value-flow 无法闭合时：

- claim 保持 `pending`，且不得让 `target_explicitness` 高于 `source_explicitness`，
  `explicitation_justified=false`；
- 中文不得比英文增加 scope、时序或触发条件的明确程度；
- 不自动进入机制性改写，采用不附着于“每回合／总计／立即”等结论的保守表达；
- 可以保存公开源码观察样例，但必须继续标出来源未固定。

记录只能在 placeholder expression、调用路径、revision 和消费 symbol 都一致时复用。仅 damage
type 名称相同不构成可复用的数据流证据。

## 规范回归

- FIREBURN：固定核心源码，验证 placeholder 1 的 directional value-flow、无既有效果时即时 `1/2`、
  3 个 periodic `1/6`、总量角色，以及 `on_timeout`／`on_merge` 消费边界；把 target 改成“每回合
  `%0.2f`”会触发 forbidden assertion。
- Startling Shot：Orcs 调用点明确标为 unpinned/pending；裁决后但尚未落地的修正模板
  `%s未能命中目标；这一枪记在%s名下。` 覆盖可见姓名／“某物”与“他的”／“她”／“它的”的
  全部六个组合，并冻结每个完整句；女性分支明确为“格鲁什未能命中目标；这一枪记在她名下。”。
  当前生产 `tome-orcs.lua:5105` 的 target 仍是 `%s的%s射击打偏了`；只有 DLC required source
  已固定且生产 target 与冻结模板一致时，才可将 composition 转为 `confirmed`。

Phase 3 全仓回扫、批量 registry 生成、模型行为 gate 和生产 Lua 修复均不属于本规范。
