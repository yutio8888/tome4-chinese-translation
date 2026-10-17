# Opus 5.5 审阅发行复核方案

mode: review_only
change_class: standard
review_contracts: [code_legacy_v1]

用户要求：将既有方案交给 Opus 5.5 审阅修订，分析是否复杂或冗余、是否适合 AI 全程独立完成，给出反馈。最终目标为发布汉化版本，非独立研究报告。

本任务只审阅未实施的规划文档，不修改运行中的翻译流程、角色、契约或工具，按纯文档方案审阅归为 standard。REVIEWER 只读返回具体反馈及最小充分修订建议，不自行编辑。主代理完成裁决、归档与 review_only DONE 后，按普通有界文档维护入口落实获采纳建议、交付用户；这不代表启动生产复核或发布。

候选是 PLAN-SNAPSHOT.md 的完整方案，CODE_DIFF-REVIEW-0-1.patch 将其作为独立新文档相对空基线呈现；仅为可复现审阅视图，不声称实际仓库刚被清空或重建。候选路径 docs/full-translation-review-plan-20261013.md。允许修改任务内容文件：无。

AC1 审查步骤对汉化发布目标的必要性、重复工作、成本规模及最小足够流程；不把复杂度本身等同缺陷。
AC2 分析 AI 可自主完成、需先验证环境能力、依赖用户实质决定或授权的工作；不能把未实际验证的 GUI/运行能力宣称可用或不可用。区分一次性环境准备与逐批人工依赖。
AC3 核对规则硬约束与方案自加要求；建议简化不得悄悄削弱 AGENTS/活跃契约，不为无关研发扩大范围。用户要求全量复核，应保留每个发行适用条目的可追溯覆盖。
AC4 每项问题给明确文档位置、源码/规则/上下文证据、可观察影响及具体最小修订方向；指出有条件可行性，不输出无证据数量或工期承诺。
AC5 主代理明确 confirmed/pending/advisory 裁决，保留原始反馈及是否采纳；review_only 的 DONE 表示审阅意见交付，不代表方案已通过无修改验收。

允许读取：本 task 的 SPEC.md、PLAN-SNAPSHOT.md、CODE_DIFF-REVIEW-0-1.patch；AGENTS.md；.ai/roles/reviewer.md；docs/agent-workflow.md 的验证矩阵和完成/复审章节；docs/paseo-orchestration-v2-contract.md；docs/paseo-translation-context-review-v2-contract.md；tools/orchestration/README.md；i18n/README.md 中 production/build/publish 配置与命令；i18n/versions/tome-1.7.6.json；候选所引 tools/i18nlib/production_review*.py、cli_production.py、build.py、publish.py 及这些模块的直接依赖；tests/i18n 中与上述行为直接相关的现有测试；必要时只读查看仓库根已有运行入口。

禁止：网络、写入/创建/删除任何文件、stage/commit、派生子代理、运行生产命令/构建/完整测试、读取其他任务/.ai/reviews/.artifacts 或既有质量 findings。不全面审核源码，只核对方案中与现有工具能力/流程约束有关的主张。

输出严格遵守 REVIEWER normal_review 格式，每项 ID / Severity / File / Location / Problem / Evidence / Impact / Recommended fix，末尾 VERDICT: PASS|CHANGES_REQUIRED。尽量集中为 4–8 项关键意见；简化建议、AI 可行性与需保留的约束写入这些字段，不增加额外字段或无结构的总结。
