# 受控变异 UI/日志 Repeat C

状态：重复契约已冻结，等待四路线独立推理。

日期：2026-08-27

本实验是 `controlled-mutation-ui-log-replication-v2` 的第三次、逐字节相同运行。Run B 中 Gemini 对 R007、R008 的主要检测状态从漏报翻转为命中，触发了预注册的 Run C 条件。

Run C 直接读取 Run A 已提交的 `HOLDOUT.json`、`PROMPT.md` 和 `REVIEWER-SCHEMA.json`，不复制、不改写、不重新排序；sealed `REFERENCE.json` 与四个 source-verified controls 同样沿用 Run A。候选模型只能看到输入、prompt 和 schema，不读取 reference、source verification、Run A/B 候选或计分结果。

四条路线、模型、effort、CLI 版本、无讨论和无 smoke 约束与 Runs A/B 相同。新目录只保存 Run C 自己的 RAW、候选、裁决、计分和三轮比较，不覆盖历史产物。

主要指标是每条路线在每个注入变异上的三轮原子主张检出频率。次要指标报告 FINDING/UNCERTAIN 置信度类别、A/B/B/C/A/C 两两翻转、controls 候选以及每路线三轮 union/intersection。Run C 完成后按预注册规则停止本设计下的重复推理；任何 Run D 或扩样必须另建并冻结实验。
