# 受控变异 UI/日志小型重复 v2

状态：抽样、直接源码核验、变异与推理契约冻结中。

日期：2026-08-27

这是 `controlled-mutation-reviewer-v1` 的小型 fresh-category replication。新总体仅使用未进入旧 pilot/v1 的 P2 UI/战斗日志终态，活动路线仍为 Codex GPT-5.6 Sol high、Claude Code Opus 5 medium、Pi/Z.ai CN GLM-5.3 Flash high、agy Gemini 3.7 Flash high。Fable 与 Advisor 不参与。

排除旧实验后共有 9 条 eligible revisions。Instant Channeling 的短错误日志与已选完整 tooltip 属于同一机制，预先排除短日志以避免重复证据；剩余 8 条全部入组，其中 4 条应用预注册变异、4 条保持 source-verified control。

与 v1 不同，本轮没有把 `DONE` 终态自动视为 clean。`SOURCE-VERIFICATION.json` 对八条完整目标逐条绑定底层源码及 SHA-256。Startling Shot 历史终态会组合成“角色的他的/她的射击”，因此仅在实验 fixture 中先修正为 `%s故意打偏了%s的射击。`，再作为 control；生产翻译不在本实验中修改。

模型只读取 `HOLDOUT.json`、`PROMPT.md` 与 schema。`REFERENCE.json`、`SOURCE-CONTROLS.json`、`SOURCE-VERIFICATION.json`、`SAMPLING.json` 以及其他路线输出在全部独立推理完成前保持 sealed。

Prompt 与 v1 保持相同判定口径，只把机械数量约束由 24 条改为 8 条，并把本类别相关的“资源/状态身份”加入检查重点。
