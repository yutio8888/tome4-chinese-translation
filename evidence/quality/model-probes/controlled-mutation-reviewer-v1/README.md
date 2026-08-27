# 受控变异 REVIEWER 比较 v1

状态：抽样、变异与推理契约冻结中。

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
