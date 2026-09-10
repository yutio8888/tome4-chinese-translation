# 已弃用文档（deprecated）

本目录收纳**已被现行流程取代、但仍有历史查证价值**的设计稿、阶段计划、一次性交接与
早期评测资产。这些文档**不再作为任何操作依据**：其中描述的命令、门禁、阈值和状态
快照多数已经失效，照做会与当前工具链冲突。

需要知道「现在该怎么做」时，一律以下列现行文档为准：

| 用途 | 现行文档 |
|---|---|
| 最高规则与硬约束 | [`AGENTS.md`](../AGENTS.md) |
| 每批操作入口与生效裁决表 | [`docs/baseline-batch-runbook-2026-09-06.md`](../docs/baseline-batch-runbook-2026-09-06.md) |
| 编排脚本用法与逐批流程 | [`tools/orchestration/README.md`](../tools/orchestration/README.md) |
| 工作流与验证矩阵 | [`docs/agent-workflow.md`](../docs/agent-workflow.md) |
| WP2-Lite 管线设计 | [`docs/translation-production-review-v2-lite-plan.md`](../docs/translation-production-review-v2-lite-plan.md) |
| 编排契约 | [`docs/paseo-orchestration-v2-contract.md`](../docs/paseo-orchestration-v2-contract.md) |
| 表层审核契约 | [`docs/paseo-translation-surface-screen-v1-contract.md`](../docs/paseo-translation-surface-screen-v1-contract.md) |
| 交叉复核契约 | [`docs/paseo-translation-context-review-v2-contract.md`](../docs/paseo-translation-context-review-v2-contract.md) |
| 术语 | [`TERMINOLOGY.md`](../TERMINOLOGY.md) |
| 操作陷阱 | [`docs/lessons-learned.md`](../docs/lessons-learned.md) |

与 [`archive/`](../archive/README.md) 的区别：`archive/` 收纳的是 **pi CLI 时代的路由层
资产**（Skill、subagent、旧契约），本目录收纳的是**被后续版本取代的设计与阶段文档**。

## 清单与取代关系

### 一次性交接与阶段快照（状态已过期）

| 文档 | 弃用原因 |
|---|---|
| `docs/production-review-handoff-2026-09-05.md` | 其中「未恢复无界连续审核」的边界已被维护者的常驻连续审核授权取代；所载队列计数是 2026-09-05 快照 |
| `docs/p2-tome-texts-handoff-2026-08-23.md` | P2 阶段交接，已完成 |
| `docs/p2-tome-texts-handoff-2026-08-25.md` | 同上 |
| `docs/release-plan.md` | 早期发布计划，与当前逐批证据链流程不一致 |
| `docs/paseo-lane-label-compat-20260905.md` | lane 标签兼容问题已在 `dispatch_surface.py` 落地，无需单独文档 |
| `docs/paseo-contextual-envelope-freeze-backlog.md` | 冻结信封的待办已全部实现 |

### 审核工具优化专项（P1–P6，已全部完成并落地）

| 文档 | 弃用原因 |
|---|---|
| `docs/review-pipeline-and-tooling-optimization-plan.md` | 六项优化已完成；结论已并入 runbook 与编排脚本 |
| `docs/review-pipeline-and-tooling-optimization-p1..p6-results.md` | 同上，结果文档仅存历史 |
| `docs/review-throughput-optimization-20260905.md` | 吞吐优化已执行完毕 |
| `docs/review-throughput-analysis-20260905.md` | 其分析结论已被后续实测（队列重放 314.8s→125.4s）取代 |
| `docs/production-review-batch-limit-upgrade-proposal-v1.md` | 批次上限提案已落定为每批 80 条 |

### 早期质量评测体系（已被两轮审核 + 裁决流程取代）

| 文档 | 弃用原因 |
|---|---|
| `docs/translation-quality-evaluator-v2.md` | evaluator 分层评测体系未进入生产；现行为表层+交叉复核两轮 |
| `docs/translation-quality-evaluator-layer-v1.md` | 同上 |
| `docs/translation-quality-evaluator-selection-v1.md` | 评测器选型，未采用 |
| `docs/translation-quality-evaluator-selection-lite-v1.md` | 同上 |
| `docs/evaluator-selection-full-impl-discard-manifest.md` | 明确记录该实现被弃用的清单 |
| `docs/translation-quality-facts-study-v1.md` / `-v2.md` / `-report-v1.md` | 事实抽取研究，未进入生产 |
| `docs/translation-quality-offline-closure-plan.md` | 离线收敛方案未采用 |
| `i18n/prompts/pi-quality-curator-v1.md` | 无任何代码引用 |
| `i18n/prompts/pi-quality-facts-author-v3.md` | 同上 |
| `i18n/prompts/pi-quality-gold-adjudication-v2.md` | 同上 |
| `i18n/prompts/pi-quality-gold-review-v2.md` | 同上 |

### 早期基础设施契约与设计稿

| 文档 | 弃用原因 |
|---|---|
| `docs/localization-infra-contract-v0.1.md` | v0.1 本地化基础设施契约，已被 WP2-Lite catalog/queue/migration 取代 |
| `docs/localization-infra-contract-v0.1-migration-004.md` | 一次性迁移记录 |
| `docs/localization-infra-contract-v0.1-migration-effect-desc.md` | 同上 |
| `docs/localization-infra-contract-v0.1-migration-g10.md` | 同上 |
| `docs/translation-production-catalog-queue-v1-plan.md` | catalog/queue v1 计划，已实现并被 v2-lite 计划取代 |
| `docs/grok-parallel-translation-review-design.md` | 并行审核设计稿，未采用（现行为 4 lane + 单 contextual） |
| `docs/dsh-orchestration-compat-v1-contract.md` | 标注「提议，未启用」；DSH 后端从未启用 |
| `docs/semantic-claim-runtime-composition-v1.md` | 运行时拼接的语义主张处理已并入 `freeze_workset.py` 的归因类 |
| `docs/translation-punctuation-convention-proposal-v1.md` | 提案；实际生效的标点裁决见 runbook 的生效裁决表 |

## 曾列入弃用、经门禁验证后撤回的文件

`i18n/prompts/pi-quality-facts-study-{a,b,c,d,f,l,n}.md` 一度被列入本目录，
理由是字面量文件名在全库无任何引用。实际上 `tools/i18nlib/facts_study.py:317` 的
`load_arm_prompt()` 是按 arm 字母**动态拼路径**加载它们的
（`f"pi-quality-facts-study-{arm.lower()}.md"`），移动后 `04-quality-facts-unit-tests`
门禁报 26 个错误。已全部撤回原位。

教训：判断文档是否可移动时，只查字面量文件名不够，还要查按参数拼接的路径；
移动后必须跑一遍完整 `tools/ci-gates.sh` 再提交。
