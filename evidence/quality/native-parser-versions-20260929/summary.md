# 原生 parser 版本维护（2026-09-29）

用户在审核369前把 Claude Code 升级到 2.1.284。`review_lifecycle.py` 的 `CLAUDE_NATIVE_VERSIONS` 只收
2.1.259 / 2.1.280，审核369两个 contextual 的 `harvest --native-log` 因此报 `unsupported Claude version`。
当批的处理：临时副本只给白名单加 2.1.284，提取 raw 后走 `--raw` 收取（`native_extract_v284.py`）。

改动：
- `CLAUDE_NATIVE_VERSIONS=('2.1.259','2.1.280','2.1.284')`，其他版本仍拒绝。Codex 白名单不变（369 批 5 个 surface lane 仍为 0.156.0，直接收取成功）。
- 测试负例加入相邻版本 2.1.283 与 2.1.285；README 同步。
- 2.1.284 的记录结构与 2.1.280 相同，包括归档时末尾追加的单条 `cost-state`，parser 逻辑无需改动。

验证：
- `tests.i18n.test_review_lifecycle` 76 项通过。
- 审核369的 2 份真实 Claude 2.1.284 会话（均已归档，末尾带 cost-state）用新 parser 解析，
  提取的 bytes 与当批 `--raw` 收取的 raw 完全一致，见 `real-log-check.json`。
- `tools/ci-gates.sh --skip-build` 16/16 通过（不改 addon 输出，按矩阵跳过构建），见 `gates-results.json`。首跑因写 summary.md 改动工作树而报 gate binding changed，文件就位后重跑通过。

提交时机：审核369已 finalize 并推送（5bc69889），无活动批次。
