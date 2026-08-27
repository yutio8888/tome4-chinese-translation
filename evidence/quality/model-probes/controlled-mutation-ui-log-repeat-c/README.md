# 受控变异 UI/日志 Repeat C

状态：完成。

日期：2026-08-27

本实验是 `controlled-mutation-ui-log-replication-v2` 的第三次、逐字节相同运行。Run B 中 Gemini 对 R007、R008 的主要检测状态从漏报翻转为命中，触发了预注册的 Run C 条件。

Run C 直接读取 Run A 已提交的 `HOLDOUT.json`、`PROMPT.md` 和 `REVIEWER-SCHEMA.json`，不复制、不改写、不重新排序；sealed `REFERENCE.json` 与四个 source-verified controls 同样沿用 Run A。候选模型只能看到输入、prompt 和 schema，不读取 reference、source verification、Run A/B 候选或计分结果。

四条路线、模型、effort、CLI 版本、无讨论和无 smoke 约束与 Runs A/B 相同。新目录只保存 Run C 自己的 RAW、候选、裁决、计分和三轮比较，不覆盖历史产物。

主要指标是每条路线在每个注入变异上的三轮原子主张检出频率。次要指标报告 FINDING/UNCERTAIN 置信度类别、A/B/B/C/A/C 两两翻转、controls 候选以及每路线三轮 union/intersection。Run C 完成后按预注册规则停止本设计下的重复推理；任何 Run D 或扩样必须另建并冻结实验。

## 结果

| 路线 | Run A | Run B | Run C | 三轮检出机会 | controls A/B/C |
| --- | ---: | ---: | ---: | ---: | --- |
| Codex / GPT-5.6 Sol high | 4/4 | 4/4 | 4/4 | 12/12 | 全部 OK |
| Claude Code / Opus 5 medium | 3/4 | 3/4 | 2/4 | 8/12 | 全部 OK |
| Pi / Z.ai CN / GLM-5.3 Flash high | 3/4 | 3/4 | 4/4 | 10/12 | 全部 OK |
| agy / Gemini 3.7 Flash high | 2/4 | 4/4 | 4/4 | 10/12 | A/B 全部 OK；C 为 3/4 OK |

Run B → C 有两个主要检测翻转：Opus 的 R008 从正确 `UNCERTAIN` 变为 `OK`，GLM 的 R007 从 `OK` 变为 `FINDING`。Gemini 保持 Run B 对 R007、R008 的命中。三轮、四路线合计下，R001 与 R005 均为 12/12，R007 为 6/12，R008 为 10/12；不稳定性集中在条件主体和运行时持续时间两项。

Gemini 在 Run C 对 source-verified control R003 提出一个额外 finding，认为“有一个精神护盾”遗漏 active。固定源码 `gestalt.lua` 的绑定 SHA-256 为 `a9467b5e48458013d77dce1a687e79ec9eccad178746db4efe086075a0d57184`；`on_pre_use` 实际检查现存 `EFF_PSI_DAMAGE_SHIELD`，现存效果即为 active shield，且译文保持 `Gestalt AND (shield OR Improved Gestalt off cooldown)` 分组。因此该项经源码驳回，是 48 个“路线 × control × run”机会中唯一的 control 候选，不是新发现的自然缺陷。

三轮结果只提供逐条频率：Codex 12/12、Opus 8/12、GLM 10/12、Gemini 10/12 不能解释为总体稳定排名。按预注册完成规则，本八条设计停止重复推理；若继续估计方差、扩样或做 reviewer × translation-origin 比较，必须另建并冻结新实验。

Claude 的 Run C 全部审核 assistant 消息均报告 `claude-opus-5`，fallback event/block 为 0；聚合 `modelUsage` 仍包含少量 Haiku 辅助开销。agy envelope 仍不报告 runtime model identity。

启动时，并行权限审查拒绝了 GLM 子调用，但已并发发出的 Gemini 调用随后正常完成。该权限层事件不计模型成绩；在用户明确永久授权四家服务后，已成功的 Gemini RAW 被原样保留且未重采样，其余三条路线各运行一次。

完整结构化三轮比较见 `RESULT.json`，Run C 原子匹配与 R003 源码裁决见 `ADJUDICATION.json`。
