# 已修改译文审核统一台账（2026-09-23）

本台账以 4144 个 inventory entry-ID 为母表，只归并已有覆盖、claim、观察和待确认，不新增语义裁决，不表示生产 `DONE_VERIFIED`。

## 统计

- 完整逐条审核并集：3836/4144；尚无完整逐条审核：308。局部术语/实验校准单列，不冒充完整审核。
- canonical claims：714；有效状态：advisory=76, confirmed=110, confirmed_provisional=417, pending=108, refuted=3。
- raw observations：4532；未显式映射：3050。不以关键词或同 entry 状态并集强行归并。
- ABC groups 1–14：560 条逐条覆盖、431 个累计 canonical defects；groups 15–20 未运行。
- ABC G04–G14 的 105 个 pending O 均按 ANON 映射恢复 entry/作者原文并连到显式 P；calibration P01–P11 全部单列，用户口径仅作用于 P01/P05/P09 及已明确映射的旧 D。
- 来源 local-ID 未闭合：977 条，均在 `SOURCE-ACCOUNTING.json` 与 `BACKLOG.json` 保留具体路径、local-ID 和原因；另有 5 条结构化观察缺明确 entry 关联，未作语义猜配。
- 92 份有效 cross 报告均建立了 source-local accounting；其中 336 个来源块以原文保留为 `unresolved`，不用 coverage 或 STATE summary 代填。覆盖引用、已解析 claim 与待解析块分别计数。
- 未识别格式采用原文保底，状态为 `unknown`，并单列 `source_local_parsing_pending`。这会增加待整理记录数，不代表新发现同等数量的译文问题，也不影响已完成逐条审核的覆盖数。

## 文件与恢复

`COVERAGE.json/.csv` 保存真实 input/output 和分层覆盖；`FINDINGS.json` 分开 canonical claims、raw observations 与 unmapped records；`SOURCE-ACCOUNTING.json` 的 included 只由具体 output refs 计算，哈希本身不算消费内容；`BACKLOG.json/.csv` 分列未覆盖、pending、未交叉疑点、未映射及 source-local 缺口；`SOURCE-MANIFEST.json` 保存所有输入哈希；`VALIDATION.json` 保存反例和 11190 文件基线检查。

运行 `python3 evidence/translation-audit/all-modified-review-20260922/reconciled-20260923/generate.py` 重放；追加 `--check` 做无写比较。

旧 `STATE.json`、`PROGRESS.md`、`HUMAN-REVIEW.md`、报告和实验均为历史快照。交叉报告按 `raw_output_path`/result dispatch/frozen input 连接，不猜编号；`sol-091-01` 无效，`sol-091-02` 生效。Flash 开发参考沿 AB claim，留出读取实际 `HOST-HOLDOUT-INITIAL.json`，run 按围栏 JSON 与 RUN-LEDGER。用户三边界只校准 `abc:g12:D08`、`abc:g11:D14`、`abc:g11:D08`，不改历史状态或同 entry 其他 claim。
