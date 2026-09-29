# 当前统一入口

当前覆盖、问题与待确认台账见 [reconciled-20260923/README.md](reconciled-20260923/README.md)。机器入口为该目录的 `COVERAGE.json`、`FINDINGS.json`、`BACKLOG.json` 和 `VALIDATION.json`；逐来源/逐 claim 纳入情况见 `SOURCE-ACCOUNTING.json`，输入哈希见 `SOURCE-MANIFEST.json`，可用 `generate.py` 重放或以 `generate.py --check` 做无写确定性比较。

`FINDINGS.json` 分开保存 canonical claim、原始 observation 与未映射记录；当前有效状态只按已有显式 crosswalk／adjudication 作用到对应 claim，不以同一 entry 的状态并集制造冲突或覆盖其他 claim。

当前完整逐条审核覆盖为 3836／4144，尚有 308 条未完整审核。已有明确映射的 claim 共 714 项，其中 pending 108 项；其他未映射观察与来源待解析块单列，不作为新增确认错译。

主审标题／advisory 字段、ABC 原始标签与宿主裁决分层、AB 显式多 entry 关联，以及 92 份 cross 报告的 source-local 记录已纳入重放。对仍未识别的 entry 观察块保留原文、来源行号和 `unknown`/`unresolved` 状态，并列入 `source_local_parsing_pending`；不以覆盖引用或 STATE 总数替代 claim 内容，也不猜配状态。

最后独立复审的结论保留为 `CHANGES_REQUIRED`；其 R04-01／R04-02 已在全部子代理归档后，由主代理完成有界原文保底修补和机械验证。该修补未再次独立复审，不冒充独立 PASS。可读问题与待办索引见 [FINDINGS.md](reconciled-20260923/FINDINGS.md)。

本目录原有 `STATE.json`、`PROGRESS.md`、`HUMAN-REVIEW.md`、旧报告与实验均保留为历史快照；其中的 remaining、covered 或 dispatched 字段不是当前统一事实，不应覆盖已落盘但未回填的结果。本入口不表示生产 `DONE_VERIFIED`，也不把模型报告或实验 reference 自动视为人工真值。
