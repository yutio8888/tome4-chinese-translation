# 文档索引

本索引说明每份文档的**现行状态**，避免照着过期文档操作。
已被取代的文档统一收在 [`deprecated/`](../deprecated/README.md)；
pi CLI 时代的路由层资产收在 [`archive/`](../archive/README.md)。

## 一、现行操作依据（改动前必读）

| 文档 | 用途 |
|---|---|
| [`AGENTS.md`](../AGENTS.md) | 最高规则与硬约束，与其他文档冲突时以本文为准 |
| [`baseline-batch-runbook-2026-09-06.md`](baseline-batch-runbook-2026-09-06.md) | **当前操作入口**：逐批命令顺序、生效裁决表、已知陷阱 |
| [`../tools/orchestration/README.md`](../tools/orchestration/README.md) | 编排脚本清单与每批流程；哪些脚本已废弃 |
| [`agent-workflow.md`](agent-workflow.md) | 工作流与验证矩阵；门禁触发条件 |
| [`lessons-learned.md`](lessons-learned.md) | 实际踩过的操作陷阱，按需查询 |
| [`../TERMINOLOGY.md`](../TERMINOLOGY.md) | 术语库使用规则 |

## 二、现行契约（工具会校验，改动需同步改代码）

| 文档 | 校验方 |
|---|---|
| [`paseo-orchestration-v2-contract.md`](paseo-orchestration-v2-contract.md) | `tools/paseo_contract_check.py` |
| [`paseo-translation-surface-screen-v1-contract.md`](paseo-translation-surface-screen-v1-contract.md) | `dispatch_surface.py`、`surface_screen_result_check.py` |
| [`paseo-translation-context-review-v2-contract.md`](paseo-translation-context-review-v2-contract.md) | `dispatch_contextual.py`、`contextual_lane_manifest.py` |
| [`paseo-clause-test-coverage.md`](paseo-clause-test-coverage.md) | `tools/paseo_contract_check.py` |

## 三、现行设计说明

| 文档 | 说明 |
|---|---|
| [`translation-production-review-v2-lite-plan.md`](translation-production-review-v2-lite-plan.md) | WP2-Lite 管线设计：catalog、队列、批次、证据与修复边界 |
| [`runtime-key-collisions.md`](runtime-key-collisions.md) | 运行时键冲突的成因与门禁 `06-runtime-collision-scan` 的依据 |
| [`project-roadmap.md`](project-roadmap.md) | **历史阶段路线图**；当前入口已移至 runbook |

## 四、已过时但仍被代码引用（**勿作操作依据**）

这些文档不再描述当前流程，但 `tools/` 或 `tests/` 中仍有路径引用，移动会破坏契约校验
或回归测试。查阅时请只把它们当作被引用代码的说明，不要照其中的流程操作。

| 文档 | 引用方 |
|---|---|
| [`paseo-translation-context-review-v1-contract.md`](paseo-translation-context-review-v1-contract.md) | `pi_tmux.py`、`paseo_contract_check.py`（现行交叉复核用 v2） |
| [`p1-execution-plan.md`](p1-execution-plan.md) | `tools/p1_select_batch.py` |
| [`translation-quality-system.md`](translation-quality-system.md)、[`translation-quality-phase-1.md`](translation-quality-phase-1.md) | `tools/i18nlib/quality.py` |
| [`translation-quality-evaluator-v3.md`](translation-quality-evaluator-v3.md) | `tests/i18n/test_toolchain_contracts.py` |
| [`terminology-review-round-2.md`](terminology-review-round-2.md) | `tools/audit_dynamic.py`、`test_terminology_inventory.py` |
| [`translation-review-production-convergence-spec.md`](translation-review-production-convergence-spec.md) | `tools/translation_review_ledger.py` |
| [`semantic-claim-runtime-composition-v1.md`](../deprecated/docs/semantic-claim-runtime-composition-v1.md) | 已移入 deprecated；其结论已并入 `freeze_workset.py` 的归因类 |

同类情形还有 `i18n/prompts/pi-*.md` 与 `i18n/quality/rubric-v{1,2,3}.md`：
它们服务于 pi 时代的质量工具（`pi_quality.py`、`quality_v2.py`、`quality_v3.py`），
现行两轮审核不使用，但删除或移动会破坏这些工具与其回归测试。
