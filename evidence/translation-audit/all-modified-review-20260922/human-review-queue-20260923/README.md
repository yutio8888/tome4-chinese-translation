# 统一人工批阅队列（合并索引）

本目录把 campaign 期间分散的"复核发现/待人工决定项"合并成一份可逐条批阅的队列。
**只做索引、原文/译文关联和 Sol 原始 verdict 挂接，不新增语义裁决。**

## 文件

| 文件 | 说明 |
| --- | --- |
| `HUMAN-REVIEW-QUEUE.md` | 逐条批阅入口，按 entry 分组。每条含原文、现译、来源层、状态、要点/人工待决、raw verdict 详情，并留"决定"空列。 |
| `HUMAN-REVIEW-QUEUE.json` | 同内容的完整结构化记录；`records[]` 每条都有 `human_decision`/`human_note`/`human_decided_at`（默认 null），以及 `raw_campaign_verdicts[]` 原始 Sol verdict 参考。 |
| `SUMMARY.json` | 生成来源哈希、分层统计、缺口提示。 |

生成器：`../build_human_review_queue.py`（可重放；只读来源）。

## 合并来源

| 层 | 来源 | 说明 |
| --- | --- | --- |
| `human_review_md` | `../HUMAN-REVIEW.md` | batch-001–091 的转录人工队列；含多 entry 合并行与"标题即条目"的 Lore 段。 |
| `cross_092` | `../reports/sol-092-01.md` | batch-092（entry-03058）交叉结论，尚未转录进 HUMAN-REVIEW。 |
| `batch_093` | `../reports/gemini-093-01.md` | 初审有疑点/细微观察的 6 条；**交叉核验尚未派发**。 |
| `batch_094` | `../reports/gemini-094-01.md` | 初审有疑点/细微观察的 4 条；**交叉核验尚未开始**。 |
| `remaining_review` | `../remaining-review-20260923/RESULTS.json` | 补审 308 条中的 108 项 Flash 疑点 + 12 项 Sol 新增观察 + 1 项 upstream。 |
| `campaign_state_untracked` | `STATE.json` raw verdict | 兜底：若某 entry 有 Sol verdict 却未进入任何人工行，则补录（本次运行无此情况）。 |

## 未合并

- `../reconciled-20260923/FINDINGS.json` 的 714 canonical claims（实验台账，`ab`/`abc`/`pilot`/`flash-holdout`/`cal10` 来源），及其 3050 条未映射 raw observations。它们是另一条工作流，有自己的 ledger，未并进本队列以免混淆 claim 身份与状态。

## 状态口径

- 状态标签原样复制模型结论，不是人工事实。
- `HUMAN-REVIEW.md` 单行可能合并多个 entry（如 `entry-01706 / 01709 / …`）或一个 entry 范围（`entry-00393–00400`）；JSON 记录用 `entry_ids[]` 保留全部，MD 按首个 entry 归组。
- `human_review_md` 的 `confirmed` 同时可能指"确认该条为问题"或"确认该条无缺陷"，需按要点文字判断；本队列不做极性过滤。

## 批阅方式

在 `HUMAN-REVIEW-QUEUE.json` 对应记录里填 `human_decision`（如 `fix` / `no_change` / `needs_source` / `defer`）、`human_note`、`human_decided_at`。
决定写入后，译文修复属于新的有界工作集，不回写或删除本队列及旧审核统计。
