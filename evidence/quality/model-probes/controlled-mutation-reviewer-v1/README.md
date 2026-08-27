# 受控变异 REVIEWER 比较 v1

状态：完成。

日期：2026-08-27

本实验以预算受控的方式测试 reviewer 对客观机制错误的检测能力。它不再包含 Fable 5 或 Advisor；后续活动路线固定为：

- Codex CLI / GPT-5.6 Sol / high；
- Claude Code CLI / Claude Opus 5 / medium；
- Pi / Z.ai CN / GLM-5.3 Flash / high；
- Antigravity CLI (`agy`) / Gemini 3.7 Flash / high。

已完成实验中的 Fable/Advisor RAW 保留为历史证据，不删除、不重算，也不进入本实验结果。

## 样本与标签

选择器从 Paseo snapshot 的 P2 机制/状态终态 contextual revisions 中排除上一轮 20 条样本，再按冻结 seed 取 SHA-256 排名最低的 24 条。奇数选择位应用一条预注册、可逆且有源码证据的机制变异，偶数位保持历史终态目标不变；随后独立打乱为 `C001`–`C024`。

`REFERENCE.json` 记录的是 12 条注入变异与 12 条未变异 control，不声称所有 control 天然绝对无缺陷。主要指标是对注入原子缺陷的命中；模型若在 control 或 mutant 上提出其他问题，必须另做源码裁决，不能机械计为误报或命中。

模型只能读取 `HOLDOUT.json`、`PROMPT.md` 和输出 schema；不得读取 `REFERENCE.json`、`SOURCE-CONTROLS.json`、`SAMPLING.json` 或其他路线输出。

构建器只对历史 `fixed_context` 中的本机源码仓库前缀做机械脱敏，保留仓库内逻辑路径；若仍出现 `/home/` 或 `/Users/` 绝对路径则拒绝生成。

## 结果

| 路线 | 变异原子命中 | FINDING-only | 未变异 control 候选 | 经源码驳回的误报 |
| --- | ---: | ---: | ---: | ---: |
| Codex / GPT-5.6 Sol high | 12/12 | 12/12 | 1 | 0 |
| Claude Code / Opus 5 medium | 11/12 | 10/12 | 1 | 0 |
| Pi / Z.ai CN / GLM-5.3 Flash high | 12/12 | 12/12 | 0 | 0 |
| agy / Gemini 3.7 Flash high | 11/12 | 11/12 | 0 | 0 |

主要指标按预注册规则把 `FINDING` 和陈述正确原子疑点的 `UNCERTAIN` 都视为检测：Opus 对 C023 正确指出 `8%` 等值边界疑点，因此该项计入 11/12；若只计 `FINDING`，Opus 为 10/12。Opus 唯一漏掉 C005 的“结束时一次结算 vs 每回合”，Gemini 唯一漏掉 C023 的“至少 8% vs 超过 8%”。四路线共同命中 10/12，union 为 12/12，没有任何路线独有命中。

GLM 原始输出在 C016 多了一个空字符串字段 `vision`。原始 RAW 与首次无效 candidate 均保留；`normalize-glm-raw.mjs` 只删除这一空未知字段，不改变 ID、verdict、observation 或 evidence，也没有重新调用模型。详见 `NORMALIZATION-pi-zai-cn-glm-5.3-flash-high.json`。

Claude 的完整审核 assistant 消息全部报告 `claude-opus-5`，fallback event/block 均为 0；但 Claude Code 的聚合 `modelUsage` 另列少量 Haiku 辅助费用。这里将其披露为 CLI 辅助开销，不当成 reviewer 消息，也不声称整个 harness 从未调用低级模型。agy 的 JSON envelope 不提供 runtime model/agent 字段；Gemini 路线身份只能由冻结的 `gemini-3.7-flash-high` 请求、运行前模型列表和 RAW 共同支持，不能称为 envelope 运行时确认。

## Control 污染与历史审核残余

C008 没有注入变异，但 Codex 判为 `FINDING`，Opus 判为 `UNCERTAIN`，两者提出同一原子问题：目标把 `%d` 写成“每回合造成”的伤害。固定源码确认这是一个自然残余缺陷：`FIRE_SHIELD` 把 `eff.power` 作为 `FIREBURN.dam`，而 `FIREBURN` 先结算默认 50% 即时伤害，再把剩余伤害除以 3 作为逐回合灼烧；天赋说明也明确三回合总伤害等于初始护盾强度。因此 C008 不是误报，并从事后 clean-control 分母中移除；剩余 11 条 control 上四路均为 11/11 OK。

Paseo provenance 显示 C008 来自 `p2-ashes-status-b2-001`：候选修改者归因 GPT/Codex，终态 contextual reviewer 为 Codex GPT-5.6 Terra high，关系为 same-family-only。源码交付 commit `1262675` 引入了错误的“每回合造成”表述，并带 Claude Sonnet 5 co-author trailer。它是一个具体的历史终态漏报，但单条不能证明 GPT 家族偏差的总体发生率或方向。

完整结构化结果见 `RESULT.json`，逐条人工/源码裁决见 `ADJUDICATION.json`。

## 下一步门槛

本轮说明受控变异能区分路线盲点，也暴露了“历史终态 control 并不自动等于 clean”的构造风险。预算上暂不直接进入 reviewer × translation-origin 全因子实验；先修订 control 构造，要求沿 `DamageType` 等底层原语追踪总量/逐回合语义，再在新的机制类别做一个小型重复，用于估计单次运行方差和 control 污染率。
