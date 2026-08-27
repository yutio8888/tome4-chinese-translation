# 受控变异 UI/日志 Repeat B

状态：重复契约冻结中。

日期：2026-08-27

本实验是 `controlled-mutation-ui-log-replication-v2` 的严格原样第二次运行（Run B），用于观察单次推理波动。它直接读取 Run A 已提交的 `HOLDOUT.json`、`PROMPT.md` 和 `REVIEWER-SCHEMA.json`，不复制、不改写、不重新排序。sealed `REFERENCE.json` 与四个 source-verified controls 同样沿用 Run A。

四条路线、模型、effort、CLI 版本、无讨论和无 smoke 约束保持不变。新目录只保存 Run B 自己的 RAW、候选、计分和 A/B 对比，不覆盖 Run A。

主要指标是每路线在四个注入变异上的“原子主张命中/漏报”是否翻转；`FINDING` 与正确原子主张的 `UNCERTAIN` 差异作为次要置信度变化报告。若任一 mutation 的主要检测状态翻转，或任一 source-verified control 出现候选，则按预注册停止规则建议 Run C；否则停止重复，但不宣称方差为零。
