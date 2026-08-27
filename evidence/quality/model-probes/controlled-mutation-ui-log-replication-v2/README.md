# 受控变异 UI/日志小型重复 v2

状态：完成。

日期：2026-08-27

这是 `controlled-mutation-reviewer-v1` 的小型 fresh-category replication。新总体仅使用未进入旧 pilot/v1 的 P2 UI/战斗日志终态，活动路线仍为 Codex GPT-5.6 Sol high、Claude Code Opus 5 medium、Pi/Z.ai CN GLM-5.3 Flash high、agy Gemini 3.7 Flash high。Fable 与 Advisor 不参与。

排除旧实验后共有 9 条 eligible revisions。Instant Channeling 的短错误日志与已选完整 tooltip 属于同一机制，预先排除短日志以避免重复证据；剩余 8 条全部入组，其中 4 条应用预注册变异、4 条保持 source-verified control。

与 v1 不同，本轮没有把 `DONE` 终态自动视为 clean。`SOURCE-VERIFICATION.json` 对八条完整目标逐条绑定底层源码及 SHA-256。Startling Shot 历史终态会组合成“角色的他的/她的射击”，因此仅在实验 fixture 中先修正为 `%s故意打偏了%s的射击。`，再作为 control；生产翻译不在本实验中修改。

模型只读取 `HOLDOUT.json`、`PROMPT.md` 与 schema。`REFERENCE.json`、`SOURCE-CONTROLS.json`、`SOURCE-VERIFICATION.json`、`SAMPLING.json` 以及其他路线输出在全部独立推理完成前保持 sealed。

Prompt 与 v1 保持相同判定口径，只把机械数量约束由 24 条改为 8 条，并把本类别相关的“资源/状态身份”加入检查重点。

## 结果

| 路线 | 变异原子命中 | FINDING-only | source-verified controls |
| --- | ---: | ---: | ---: |
| Codex / GPT-5.6 Sol high | 4/4 | 4/4 | 4/4 OK |
| Claude Code / Opus 5 medium | 3/4 | 2/4 | 4/4 OK |
| Pi / Z.ai CN / GLM-5.3 Flash high | 3/4 | 3/4 | 4/4 OK |
| agy / Gemini 3.7 Flash high | 2/4 | 2/4 | 4/4 OK |

Opus 在 R008 精确指出英文/中文 3 回合与运行时 4 回合的冲突，但给出 `UNCERTAIN`；按预注册的非 `OK` 原子主张口径计为命中，FINDING-only 则不计。四路共同命中 R001 的属性身份错误和 R005 的前置条件身份错误。R007 遗漏“机械蜘蛛也必须脱离战斗”只被 Codex 发现；R008 被 Codex、GLM 和 Opus 提名，Gemini 漏掉。Union 为 4/4，四路 consensus 为 2/4。

四个直接源码核验 control 被四路全部判为 `OK`，没有候选、无需事后修正 control 标签。这说明 v1 的污染问题可以通过完整 baseline tracing 和 fixture-only 修复规避。

与 v1 只能作描述性比较：Codex 仍为 100%；GLM 从 12/12 降至 3/4，Opus 从 11/12 降至 3/4，Gemini 从 11/12 降至 2/4。只有四个新变异且每路只运行一次，因此不能把比例解释成稳定排名；它足以否定“上一轮近满分可直接外推到 UI/日志类别”。

Claude 的全部审核 assistant 消息仍为 `claude-opus-5` 且 fallback 为 0，聚合用量另列少量 Haiku 辅助开销。agy envelope 仍不提供 runtime model identity。

完整结构化结果见 `RESULT.json`，原子匹配见 `ADJUDICATION.json`。

## 下一步

若继续投入预算，优先在完全相同、继续冻结的 8 条输入上重复一次四路线推理，专门估计 R007/R008 的运行间方差；在此之前不应进入更昂贵的 reviewer × translation-origin 全因子实验。
