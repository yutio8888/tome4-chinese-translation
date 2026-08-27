# 受控变异 UI/日志 Repeat B

状态：完成。

日期：2026-08-27

本实验是 `controlled-mutation-ui-log-replication-v2` 的严格原样第二次运行（Run B），用于观察单次推理波动。它直接读取 Run A 已提交的 `HOLDOUT.json`、`PROMPT.md` 和 `REVIEWER-SCHEMA.json`，不复制、不改写、不重新排序。sealed `REFERENCE.json` 与四个 source-verified controls 同样沿用 Run A。

四条路线、模型、effort、CLI 版本、无讨论和无 smoke 约束保持不变。新目录只保存 Run B 自己的 RAW、候选、计分和 A/B 对比，不覆盖 Run A。

主要指标是每路线在四个注入变异上的“原子主张命中/漏报”是否翻转；`FINDING` 与正确原子主张的 `UNCERTAIN` 差异作为次要置信度变化报告。若任一 mutation 的主要检测状态翻转，或任一 source-verified control 出现候选，则按预注册停止规则建议 Run C；否则停止重复，但不宣称方差为零。

## 结果

| 路线 | Run A | Run B | 主要检测翻转 | controls（A / B） |
| --- | ---: | ---: | --- | ---: |
| Codex / GPT-5.6 Sol high | 4/4 | 4/4 | 无 | 4/4 OK / 4/4 OK |
| Claude Code / Opus 5 medium | 3/4 | 3/4 | 无 | 4/4 OK / 4/4 OK |
| Pi / Z.ai CN / GLM-5.3 Flash high | 3/4 | 3/4 | 无 | 4/4 OK / 4/4 OK |
| agy / Gemini 3.7 Flash high | 2/4 | 4/4 | R007、R008：漏报 → 命中 | 4/4 OK / 4/4 OK |

Codex、Opus 与 GLM 的命中集合和 verdict class 均原样复现。Opus 两轮都把 R008 的 3/4 回合冲突判为正确的 `UNCERTAIN`，因此主要非 `OK` 原子主张口径为 3/4，FINDING-only 为 2/4。Gemini 则把 Run A 中判 `OK` 的 R007 条件主体遗漏与 R008 运行时持续时间，在 Run B 均改判为 `FINDING`。

16 个“路线 × mutation”比较中有 14 个一致，主要一致率为 87.5%；两个翻转都来自 Gemini，方向均为漏报到命中。四条直接源码核验 control 在两轮、四路线中始终为 `OK`。Run B 的四路 union 为 4/4，consensus 为 3/4。

预注册停止规则已经触发，因此本实验不把 Run B 单次的 Gemini 4/4 解释为稳定能力，也不再沿用 Run A 的 2/4 作稳定排名。下一步是再做一次逐字节相同的 Run C，然后报告逐条三轮检出频率；在 Run C 前不改 prompt、不扩样本。

Claude 的全部审核 assistant 消息均报告 `claude-opus-5`，fallback event/block 为 0；聚合 `modelUsage` 仍含少量 Haiku 辅助开销。agy envelope 仍不报告 runtime model identity。

完整可重建结果见 `RESULT.json`，Run B 原子匹配见 `ADJUDICATION.json`。

## 门禁与历史输入漂移

Repeat B 自身的 JSON/JSONL 解析、冻结 hash、四路 identity/schema、`RESULT.json` 字节重建和 executor fixture 基线均通过。受控变异 v1 与 Run A v2 也在生产仓库冻结 commit `1666481409f4c0d63d66e84659f6b6145d8d25d0` 的临时只读视图上通过字节重建；当前生产 HEAD 已前进，因此不能把当前 HEAD 直接传给历史 builder。

Paseo provenance snapshot 的活记录全字节重建不再成立。冻结 commit 视图下，新旧 snapshot 的 132 个 task 和完整 `summary` 仍相同，2253 个 manifest records 中 2252 个仍与活源匹配；唯一漂移是 agent metadata `bae131e1-5bf3-4707-a23e-9e7e87852e29`，由冻结时 2302 bytes / SHA-256 `a9971c5c3ffebc400789cdb5d4248259097e9fa176afcb969b2bde4027c6939d` 变为 2348 bytes / `79878d213fa213303e8a370bcff7217fafe64d3a05f193040bb4965f594edb6c`。旧字节未保存，故不能补写为 PASS。该外部 metadata 漂移不进入 Repeat B 模型输入；Repeat B 已直接验证 Run A 的 HOLDOUT、prompt、schema、reference、source verification、四个候选和 RESULT hash。
